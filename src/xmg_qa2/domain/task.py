"""Durable support-task lifecycle types and transition rules."""

from collections.abc import Mapping
from dataclasses import dataclass, replace
from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import UUID

from xmg_qa2.domain.errors import InvalidTransition, StaleStateVersion
from xmg_qa2.domain.qa import QuestionFrame


class SupportTaskStatus(StrEnum):
    NEW = "NEW"
    RUNNING = "RUNNING"
    WAITING_INPUT = "WAITING_INPUT"
    PAUSED = "PAUSED"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"


class RunStatus(StrEnum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class HumanRequestStatus(StrEnum):
    PENDING = "PENDING"
    SATISFIED = "SATISFIED"
    SUPERSEDED = "SUPERSEDED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"


class ResumeAttemptStatus(StrEnum):
    RECEIVED = "RECEIVED"
    REJECTED = "REJECTED"
    QUEUED = "QUEUED"
    APPLIED = "APPLIED"
    FAILED = "FAILED"


@dataclass(frozen=True, slots=True)
class SupportTask:
    id: UUID
    case_id: UUID
    customer_id: str
    project_id: str | None
    created_by_principal: str
    status: SupportTaskStatus
    state_version: int
    workflow_name: str
    workflow_version: str
    question_text: str
    created_at: datetime
    updated_at: datetime
    current_question_frame_id: UUID | None = None
    current_run_id: UUID | None = None
    resolved_at: datetime | None = None
    closed_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class Run:
    id: UUID
    task_id: UUID
    status: RunStatus
    workflow_version: str
    lease_epoch: int
    expected_task_version: int
    started_at: datetime
    heartbeat_at: datetime
    trace_id: str
    ended_at: datetime | None = None
    stop_reason: str | None = None


@dataclass(frozen=True, slots=True)
class HumanRequest:
    id: UUID
    task_id: UUID
    run_id: UUID
    request_version: int
    status: HumanRequestStatus
    interrupt_id: str
    target_task_version: int
    request_type: str
    prompt: str
    required_fields: Mapping[str, Any]
    created_at: datetime
    expires_at: datetime | None = None
    superseded_by_id: UUID | None = None
    satisfied_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class ResumeAttempt:
    id: UUID
    human_request_id: UUID
    reply_id: str
    principal_id: str
    target_task_version: int
    target_interrupt_id: str
    status: ResumeAttemptStatus
    received_at: datetime
    reason: str | None = None
    applied_at: datetime | None = None


_TRANSITIONS: Mapping[SupportTaskStatus, frozenset[SupportTaskStatus]] = {
    SupportTaskStatus.NEW: frozenset({SupportTaskStatus.RUNNING, SupportTaskStatus.CANCELLED}),
    SupportTaskStatus.RUNNING: frozenset(
        {
            SupportTaskStatus.WAITING_INPUT,
            SupportTaskStatus.PAUSED,
            SupportTaskStatus.RESOLVED,
            SupportTaskStatus.CANCELLED,
            SupportTaskStatus.FAILED,
        }
    ),
    SupportTaskStatus.WAITING_INPUT: frozenset(
        {SupportTaskStatus.RUNNING, SupportTaskStatus.CANCELLED, SupportTaskStatus.FAILED}
    ),
    SupportTaskStatus.PAUSED: frozenset(
        {SupportTaskStatus.RUNNING, SupportTaskStatus.CANCELLED, SupportTaskStatus.FAILED}
    ),
    SupportTaskStatus.RESOLVED: frozenset(
        {SupportTaskStatus.CLOSED, SupportTaskStatus.RUNNING}
    ),
    SupportTaskStatus.CLOSED: frozenset(),
    SupportTaskStatus.CANCELLED: frozenset(),
    SupportTaskStatus.FAILED: frozenset({SupportTaskStatus.RUNNING}),
}


def transition_task(
    task: SupportTask,
    target: SupportTaskStatus,
    *,
    expected_state_version: int,
    question_frame: QuestionFrame | None = None,
    now: datetime | None = None,
) -> SupportTask:
    """Apply a validated optimistic task transition without persistence concerns."""
    if task.state_version != expected_state_version:
        raise StaleStateVersion(
            f"expected task version {expected_state_version}, found {task.state_version}"
        )
    if target not in _TRANSITIONS[task.status]:
        raise InvalidTransition(f"cannot transition task from {task.status} to {target}")
    if (
        target is SupportTaskStatus.RESOLVED
        and question_frame is not None
        and question_frame.has_critical_pending_subquestions
    ):
        raise InvalidTransition("critical subquestions must be answered before resolution")

    changed_at = now or task.updated_at
    return replace(
        task,
        status=target,
        state_version=task.state_version + 1,
        updated_at=changed_at,
        resolved_at=changed_at if target is SupportTaskStatus.RESOLVED else task.resolved_at,
        closed_at=changed_at if target is SupportTaskStatus.CLOSED else task.closed_at,
    )
