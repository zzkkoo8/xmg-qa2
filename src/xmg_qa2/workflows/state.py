"""Serializable state passed through the bounded support graph."""

from typing import TypedDict


class WorkflowState(TypedDict, total=False):
    scenario: str
    route: str
    outcome: str
    evidence_ids: list[str]
    denial_reason: str | None
    may_resolve: bool
    steps: int
    no_progress_steps: int
    stopped: bool
