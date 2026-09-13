"""Transactional PostgreSQL repositories with optimistic fencing."""

from datetime import UTC, datetime
from typing import Any, cast
from uuid import UUID, uuid4

from sqlalchemy import update
from sqlalchemy.engine import CursorResult
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from xmg_qa2.domain.errors import StaleStateVersion
from xmg_qa2.domain.task import SupportTask
from xmg_qa2.infrastructure.db.models import (
    AnswerCheckRow,
    AnswerDraftRow,
    EvidenceRow,
    HumanRequestRow,
    OperationCommitRow,
    OutboxEventRow,
    ResumeAttemptRow,
    RunRow,
    SupportTaskRow,
)


class TaskRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_task(self, task: SupportTask) -> None:
        self.session.add(
            SupportTaskRow(
                id=task.id,
                case_id=task.case_id,
                customer_id=task.customer_id,
                project_id=task.project_id,
                created_by_principal=task.created_by_principal,
                status=task.status.value,
                state_version=task.state_version,
                workflow_name=task.workflow_name,
                workflow_version=task.workflow_version,
                question_text=task.question_text,
                current_question_frame_id=task.current_question_frame_id,
                current_run_id=task.current_run_id,
                created_at=task.created_at,
                updated_at=task.updated_at,
                resolved_at=task.resolved_at,
                closed_at=task.closed_at,
            )
        )
        self.session.flush()

    def get_task(self, task_id: UUID) -> SupportTaskRow | None:
        return self.session.get(SupportTaskRow, task_id)

    def create_run(self, run: RunRow) -> None:
        self.session.add(run)
        self.session.flush()

    def create_human_request(self, request: HumanRequestRow) -> None:
        self.session.add(request)
        self.session.flush()

    def record_resume_attempt(self, attempt: ResumeAttemptRow) -> bool:
        self.session.add(attempt)
        try:
            self.session.flush()
        except IntegrityError:
            self.session.rollback()
            return False
        return True

    def store_evidence(self, evidence: EvidenceRow) -> None:
        self.session.add(evidence)
        self.session.flush()

    def store_answer_draft(self, draft: AnswerDraftRow) -> None:
        self.session.add(draft)
        self.session.flush()

    def store_answer_check(self, check: AnswerCheckRow) -> None:
        self.session.add(check)
        self.session.flush()

    def enqueue_outbox(self, event: OutboxEventRow) -> None:
        self.session.add(event)
        self.session.flush()

    def transition_task(self, task_id: UUID, expected_state_version: int, status: str) -> None:
        result = cast(
            CursorResult[Any],
            self.session.execute(
            update(SupportTaskRow)
            .where(
                SupportTaskRow.id == task_id,
                SupportTaskRow.state_version == expected_state_version,
            )
            .values(
                status=status,
                state_version=expected_state_version + 1,
                updated_at=datetime.now(UTC),
            )
            ),
        )
        if result.rowcount != 1:
            raise StaleStateVersion(f"stale task version {expected_state_version}")

    def acquire_or_renew_lease(self, run_id: UUID, expected_epoch: int) -> int:
        next_epoch = expected_epoch + 1
        result = cast(
            CursorResult[Any],
            self.session.execute(
            update(RunRow)
            .where(RunRow.id == run_id, RunRow.lease_epoch == expected_epoch)
            .values(lease_epoch=next_epoch, heartbeat_at=datetime.now(UTC))
            ),
        )
        if result.rowcount != 1:
            raise StaleStateVersion(f"stale lease epoch {expected_epoch}")
        return next_epoch

    def commit_operation(
        self,
        *,
        task_id: UUID,
        run_id: UUID,
        operation_id: str,
        lease_epoch: int,
        task_version_before: int,
        task_version_after: int,
        operation_type: str,
        result_digest: str,
    ) -> bool:
        current_epoch = self.session.get(RunRow, run_id)
        if current_epoch is None or current_epoch.lease_epoch != lease_epoch:
            raise StaleStateVersion(f"stale lease epoch {lease_epoch}")
        self.session.add(
            OperationCommitRow(
                id=uuid4(),
                task_id=task_id,
                run_id=run_id,
                operation_id=operation_id,
                lease_epoch=lease_epoch,
                task_version_before=task_version_before,
                task_version_after=task_version_after,
                operation_type=operation_type,
                result_digest=result_digest,
                committed_at=datetime.now(UTC),
                created_at=datetime.now(UTC),
            )
        )
        try:
            self.session.flush()
        except IntegrityError:
            self.session.rollback()
            return False
        return True
