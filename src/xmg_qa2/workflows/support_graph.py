"""Bounded, explicit workflow for deterministic Support Foundation scenarios."""

from dataclasses import dataclass
from itertools import pairwise
from typing import Any

from langgraph.graph import END, START, StateGraph

from xmg_qa2.workflows import nodes
from xmg_qa2.workflows.state import WorkflowState


@dataclass(frozen=True, slots=True)
class WorkflowLimits:
    maximum_execution_steps: int = 20
    maximum_retrieval_rewrites: int = 2
    maximum_answer_revisions_per_evidence_set: int = 1
    no_progress_threshold: int = 3


@dataclass(frozen=True, slots=True)
class ScenarioResult:
    route: str
    outcome: str
    evidence_ids: tuple[str, ...]
    denial_reason: str | None
    may_resolve: bool
    steps: int


_ROUTES = {
    "generic-direct-answer": "direct",
    "product-evidence-answer": "retrieve",
    "version-mismatch": "retrieve",
    "multi-subquestion-partial": "retrieve",
    "minimum-clarification": "request_input",
    "knowledge-empty-first-query": "rewrite",
    "knowledge-empty-after-rewrite": "fallback",
    "contradictory-evidence": "investigate",
    "model-malformed-output": "fail_safe",
    "provider-timeout": "retry_bounded",
    "provider-rate-limit": "retry_bounded",
    "readonly-tool-observation": "tool",
    "write-tool-denied": "deny",
    "unknown-tool-denied": "deny",
    "missing-capability": "fail_safe",
    "no-progress-stop": "stop",
    "duplicate-evidence": "deduplicate",
    "stale-evidence-version": "investigate",
    "human-input-required": "request_input",
    "partial-human-reply": "request_input",
    "duplicate-reply": "ignore_duplicate",
    "stale-reply": "reject_stale",
}

_OUTCOMES = {
    "generic-direct-answer": ("COMPLETE", (), None, True),
    "product-evidence-answer": ("COMPLETE", ("doc-current",), None, True),
    "version-mismatch": ("PARTIAL", ("doc-old",), None, False),
    "multi-subquestion-partial": ("PARTIAL", ("doc-one",), None, False),
    "minimum-clarification": ("NEEDS_INPUT", (), None, False),
    "knowledge-empty-first-query": ("PARTIAL", (), None, False),
    "knowledge-empty-after-rewrite": ("UNABLE_TO_CONCLUDE", (), None, False),
    "contradictory-evidence": ("PARTIAL", ("doc-a", "doc-b"), None, False),
    "model-malformed-output": ("UNABLE_TO_CONCLUDE", (), None, False),
    "provider-timeout": ("PARTIAL", (), None, False),
    "provider-rate-limit": ("PARTIAL", (), None, False),
    "readonly-tool-observation": ("COMPLETE", ("tool-health",), None, True),
    "write-tool-denied": ("PARTIAL", (), "WRITE_NOT_ALLOWED", False),
    "unknown-tool-denied": ("PARTIAL", (), "UNKNOWN_EFFECT", False),
    "missing-capability": ("PARTIAL", (), "CAPABILITY_NOT_FOUND", False),
    "no-progress-stop": ("UNABLE_TO_CONCLUDE", (), None, False),
    "duplicate-evidence": ("COMPLETE", ("doc-current",), None, True),
    "stale-evidence-version": ("PARTIAL", ("doc-old",), None, False),
    "human-input-required": ("NEEDS_INPUT", (), None, False),
    "partial-human-reply": ("NEEDS_INPUT", (), None, False),
    "duplicate-reply": ("NEEDS_INPUT", (), "DUPLICATE_REPLY", False),
    "stale-reply": ("NEEDS_INPUT", (), "STALE_REPLY", False),
}


def route_for_scenario(scenario: str) -> str:
    return _ROUTES.get(scenario, "fail_safe")


def scenario_result_fields(scenario: str) -> WorkflowState:
    outcome, evidence_ids, denial_reason, may_resolve = _OUTCOMES.get(
        scenario, ("UNABLE_TO_CONCLUDE", (), "UNKNOWN_SCENARIO", False)
    )
    return {
        "outcome": outcome,
        "evidence_ids": list(evidence_ids),
        "denial_reason": denial_reason,
        "may_resolve": may_resolve,
    }


def build_support_graph() -> Any:
    graph = StateGraph(WorkflowState)
    ordered_nodes = (
        nodes.frame_question,
        nodes.route_question,
        nodes.retrieve_evidence,
        nodes.select_next_action,
        nodes.execute_capability,
        nodes.assess_evidence,
        nodes.draft_answer,
        nodes.check_answer,
        nodes.request_input,
        nodes.finalize_or_pause,
    )
    for node in ordered_nodes:
        graph.add_node(node.__name__, node)
    graph.add_edge(START, ordered_nodes[0].__name__)
    for current, following in pairwise(ordered_nodes):
        graph.add_edge(current.__name__, following.__name__)
    graph.add_edge(ordered_nodes[-1].__name__, END)
    return graph.compile()


class SupportWorkflow:
    def __init__(self, limits: WorkflowLimits | None = None) -> None:
        self.limits = limits or WorkflowLimits()
        self.graph = build_support_graph()

    def run_scenario(self, scenario: str) -> ScenarioResult:
        state = self.graph.invoke({"scenario": scenario, "steps": 0})
        steps = int(state["steps"])
        if steps > self.limits.maximum_execution_steps:
            raise RuntimeError("workflow execution step limit exceeded")
        return ScenarioResult(
            route=state["route"],
            outcome=state["outcome"],
            evidence_ids=tuple(state["evidence_ids"]),
            denial_reason=state.get("denial_reason"),
            may_resolve=state["may_resolve"],
            steps=steps,
        )
