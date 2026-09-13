"""Common provider-neutral Harness DTOs."""

from dataclasses import dataclass

from xmg_qa2.domain.capability import CapabilityDescriptor, CapabilityEffect

__all__ = ["CapabilityDescriptor", "CapabilityEffect", "InvocationContext"]


@dataclass(frozen=True, slots=True)
class InvocationContext:
    task_id: str
    case_id: str
    customer_id: str
    project_id: str | None
    principal_id: str
    run_id: str
    operation_id: str
    trace_id: str
