"""Durable HumanRequest creation and exact resume lifecycle."""

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from xmg_qa2.infrastructure.checkpoint.postgres import PostgresCheckpointAdapter
from xmg_qa2.infrastructure.db.models import (
    HumanRequestRow,
    OutboxEventRow,
    ResumeAttemptRow,
    SupportTaskRow,
)


class ResumeDecision(StrEnum):
    QUEUED = "QUEUED"
    PARTIAL = "PARTIAL"
    DUPLICATE = "DUPLICATE"
    REJECTED_STALE = "REJECTED_STALE"
    REJECTED_PRINCIPAL = "REJECTED_PRINCIPAL"


@dataclass(frozen=True, slots=True)
class ResumeResult:
    decision: ResumeDecision
    attempt_id: UUID
    missing_fields: tuple[str, ...] = ()


class TaskService:
    def __init__(
        self,
        sessions: sessionmaker[Session],
        checkpoint: PostgresCheckpointAdapter,
    ) -> None:
        self.sessions = sessions
        self.checkpoint = checkpoint

    def request_input(
        self,
        task_id: UUID,
        run_id: UUID,
        interrupt_id: str,
        request_version: int,
        expected_task_version: int,
        prompt: str,
        required_fields: dict[str, bool],
    ) -> HumanRequestRow:
        self.checkpoint.setup()
        self.checkpoint.record_operation(str(run_id), f"interrupt:{interrupt_id}")
        now = datetime.now(UTC)
        request = HumanRequestRow(
            id=uuid4(),
            task_id=task_id,
            run_id=run_id,
            request_version=request_version,
            status="PENDING",
            interrupt_id=interrupt_id,
            target_task_version=expected_task_version + 1,
            request_type="CLARIFICATION",
            prompt=prompt,
            required_fields=required_fields,
            created_at=now,
        )
        with self.sessions.begin() as session:
            task = session.get(SupportTaskRow, task_id)
            if task is None or task.state_version != expected_task_version:
                raise ValueError("task version changed before wait commit")
            task.status = "WAITING_INPUT"
            task.state_version += 1
            task.updated_at = now
            session.add(request)
            session.add(
                OutboxEventRow(
                    id=uuid4(),
                    task_id=task_id,
                    topic="human_request.ready",
                    payload={
                        "task_id": str(task_id),
                        "request_id": str(request.id),
                        "request_version": request_version,
                    },
                    created_at=now,
                )
            )
        return request

    def accept_reply(
        self,
        request_id: UUID,
        reply_id: str,
        principal_id: str,
        target_interrupt_id: str,
        target_task_version: int,
        values: dict[str, object],
    ) -> ResumeResult:
        with self.sessions.begin() as session:
            duplicate = session.scalar(
                select(ResumeAttemptRow).where(
                    ResumeAttemptRow.human_request_id == request_id,
                    ResumeAttemptRow.reply_id == reply_id,
                )
            )
            if duplicate is not None:
                return ResumeResult(ResumeDecision.DUPLICATE, duplicate.id)
            request = session.get(HumanRequestRow, request_id)
            if request is None:
                raise ValueError("human request not found")
            task = session.get(SupportTaskRow, request.task_id)
            if task is None:
                raise ValueError("support task not found")

            decision = ResumeDecision.QUEUED
            status = "QUEUED"
            reason = None
            if principal_id != task.created_by_principal:
                decision, status, reason = (
                    ResumeDecision.REJECTED_PRINCIPAL,
                    "REJECTED",
                    "PRINCIPAL_DENIED",
                )
            elif (
                request.status != "PENDING"
                or request.interrupt_id != target_interrupt_id
                or request.target_task_version != target_task_version
                or task.state_version != target_task_version
            ):
                decision, status, reason = (
                    ResumeDecision.REJECTED_STALE,
                    "REJECTED",
                    "STALE_INTERRUPT_OR_VERSION",
                )

            missing = tuple(
                sorted(
                    name
                    for name, required in request.required_fields.items()
                    if required and not values.get(name)
                )
            )
            if decision is ResumeDecision.QUEUED and missing:
                decision, status, reason = ResumeDecision.PARTIAL, "REJECTED", "MISSING_FIELDS"

            attempt = ResumeAttemptRow(
                id=uuid4(),
                human_request_id=request.id,
                reply_id=reply_id,
                principal_id=principal_id,
                target_task_version=target_task_version,
                target_interrupt_id=target_interrupt_id,
                status=status,
                reason=reason,
                received_at=datetime.now(UTC),
                created_at=datetime.now(UTC),
            )
            session.add(attempt)
            session.flush()
            if decision is ResumeDecision.QUEUED:
                session.add(
                    OutboxEventRow(
                        id=uuid4(),
                        task_id=task.id,
                        topic="workflow.resume",
                        payload={
                            "task_id": str(task.id),
                            "attempt_id": str(attempt.id),
                            "target_task_version": target_task_version,
                            "interrupt_id": target_interrupt_id,
                        },
                        created_at=datetime.now(UTC),
                    )
                )
            return ResumeResult(decision, attempt.id, missing)

    def mark_resume_consumed(self, attempt_id: UUID) -> None:
        with self.sessions.begin() as session:
            attempt = session.get(ResumeAttemptRow, attempt_id)
            if attempt is None or attempt.status != "QUEUED":
                raise ValueError("resume attempt is not queued")
            request = session.get(HumanRequestRow, attempt.human_request_id)
            if request is None or request.status != "PENDING":
                raise ValueError("human request is no longer pending")
            task = session.get(SupportTaskRow, request.task_id)
            if task is None or task.state_version != attempt.target_task_version:
                raise ValueError("task version changed before resume consumption")
            now = datetime.now(UTC)
            attempt.status = "APPLIED"
            attempt.applied_at = now
            request.status = "SATISFIED"
            request.satisfied_at = now
            task.status = "RUNNING"
            task.state_version += 1
            task.updated_at = now

    def resume_status(self, attempt_id: UUID) -> str:
        with self.sessions() as session:
            attempt = session.get(ResumeAttemptRow, attempt_id)
            if attempt is None:
                raise ValueError("resume attempt not found")
            return attempt.status

    def request_status(self, request_id: UUID) -> str:
        with self.sessions() as session:
            request = session.get(HumanRequestRow, request_id)
            if request is None:
                raise ValueError("human request not found")
            return request.status

    def task_id_for_request(self, request_id: UUID) -> UUID:
        with self.sessions() as session:
            request = session.get(HumanRequestRow, request_id)
            if request is None:
                raise ValueError("human request not found")
            return request.task_id
