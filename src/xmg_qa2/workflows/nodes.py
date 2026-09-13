"""Recognizable deterministic responsibilities in the QA workflow."""

from xmg_qa2.workflows.state import WorkflowState


def _advance(state: WorkflowState) -> WorkflowState:
    return {"steps": state.get("steps", 0) + 1}


def frame_question(state: WorkflowState) -> WorkflowState:
    return _advance(state)


def route_question(state: WorkflowState) -> WorkflowState:
    from xmg_qa2.workflows.support_graph import route_for_scenario

    return {**_advance(state), "route": route_for_scenario(state["scenario"])}


def retrieve_evidence(state: WorkflowState) -> WorkflowState:
    return _advance(state)


def select_next_action(state: WorkflowState) -> WorkflowState:
    return _advance(state)


def execute_capability(state: WorkflowState) -> WorkflowState:
    return _advance(state)


def assess_evidence(state: WorkflowState) -> WorkflowState:
    return _advance(state)


def draft_answer(state: WorkflowState) -> WorkflowState:
    return _advance(state)


def check_answer(state: WorkflowState) -> WorkflowState:
    return _advance(state)


def request_input(state: WorkflowState) -> WorkflowState:
    return _advance(state)


def finalize_or_pause(state: WorkflowState) -> WorkflowState:
    from xmg_qa2.workflows.support_graph import scenario_result_fields

    return {**_advance(state), **scenario_result_fields(state["scenario"])}
