"""Queue payload validation and checkpoint/business-state reconciliation."""

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


@dataclass(frozen=True, slots=True)
class ExecutionMessage:
    task_id: str
    run_id: str
    expected_task_version: int
    lease_epoch: int
    workflow_version: str

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> "ExecutionMessage":
        expected_keys = {
            "task_id", "run_id", "expected_task_version", "lease_epoch", "workflow_version"
        }
        if payload.keys() != expected_keys:
            raise ValueError("execution payload must contain IDs and version metadata only")
        return cls(**payload)

    def to_payload(self) -> dict[str, Any]:
        return asdict(self)


class ReconciliationAction(StrEnum):
    CONSISTENT = "CONSISTENT"
    ADVANCE_CHECKPOINT = "ADVANCE_CHECKPOINT"
    RERUN_SAFE_OPERATION = "RERUN_SAFE_OPERATION"
    PAUSE_UNSAFE_OPERATION = "PAUSE_UNSAFE_OPERATION"


def reconcile_operation(
    *,
    checkpoint_operation_id: str | None,
    business_operation_id: str | None,
    operation_is_safe_to_repeat: bool,
) -> ReconciliationAction:
    if checkpoint_operation_id == business_operation_id:
        return ReconciliationAction.CONSISTENT
    if business_operation_id is not None:
        return ReconciliationAction.ADVANCE_CHECKPOINT
    # A checkpoint-only effect is never business truth. Re-run only an explicitly
    # idempotent/read-only step; otherwise pause for safe operator handling.
    if operation_is_safe_to_repeat:
        return ReconciliationAction.RERUN_SAFE_OPERATION
    return ReconciliationAction.PAUSE_UNSAFE_OPERATION
