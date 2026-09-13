from xmg_qa2.workflows.support_graph import WorkflowLimits, route_for_scenario


def test_required_workflow_limits_are_explicit_defaults() -> None:
    limits = WorkflowLimits()
    assert limits.maximum_execution_steps == 20
    assert limits.maximum_retrieval_rewrites == 2
    assert limits.maximum_answer_revisions_per_evidence_set == 1
    assert limits.no_progress_threshold == 3


def test_route_for_known_control_scenarios_is_deterministic() -> None:
    assert route_for_scenario("product-evidence-answer") == "retrieve"
    assert route_for_scenario("write-tool-denied") == "deny"
    assert route_for_scenario("human-input-required") == "request_input"
    assert route_for_scenario("no-progress-stop") == "stop"
