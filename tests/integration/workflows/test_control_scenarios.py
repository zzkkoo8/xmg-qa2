from pathlib import Path

import pytest
import yaml

from xmg_qa2.workflows.support_graph import SupportWorkflow

SCENARIOS = yaml.safe_load(Path("tests/fixtures/qa_scenarios.yaml").read_text())["scenarios"]


@pytest.mark.parametrize("scenario", SCENARIOS, ids=lambda item: item["name"])
def test_frozen_control_scenario(scenario: dict[str, object]) -> None:
    result = SupportWorkflow().run_scenario(str(scenario["name"]))
    assert result.route == scenario["route"]
    assert result.outcome == scenario["outcome"]
    assert result.may_resolve is scenario["may_resolve"]
    assert set(result.evidence_ids) == set(scenario["evidence_ids"])
    assert result.denial_reason == scenario.get("denial_reason")
    assert result.steps <= 20
