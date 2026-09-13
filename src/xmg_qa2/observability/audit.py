"""Allow-listed audit projection; raw provider content is excluded."""

from dataclasses import asdict, dataclass
from typing import Any, cast

from xmg_qa2.observability.logging import redact


@dataclass(frozen=True, slots=True)
class SafeAuditEvent:
    task_id: str | None = None
    case_id: str | None = None
    run_id: str | None = None
    operation_id: str | None = None
    trace_id: str | None = None
    workflow: str | None = None
    workflow_version: str | None = None
    node: str | None = None
    provider_id: str | None = None
    capability_id: str | None = None
    latency_ms: float | None = None
    retry_count: int | None = None
    evidence_ids: tuple[str, ...] = ()
    outcome: str | None = None
    reason_code: str | None = None

    def safe_metadata(self) -> dict[str, Any]:
        return cast(dict[str, Any], redact(asdict(self)))
