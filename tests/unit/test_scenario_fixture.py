from pathlib import Path

import yaml

REQUIRED = {
    "generic-direct-answer", "product-evidence-answer", "version-mismatch",
    "multi-subquestion-partial", "minimum-clarification", "knowledge-empty-first-query",
    "knowledge-empty-after-rewrite", "contradictory-evidence", "model-malformed-output",
    "provider-timeout", "provider-rate-limit", "readonly-tool-observation",
    "write-tool-denied", "unknown-tool-denied", "missing-capability", "no-progress-stop",
    "duplicate-evidence", "stale-evidence-version", "human-input-required",
    "partial-human-reply", "duplicate-reply", "stale-reply",
}


def test_control_scenario_corpus_is_complete_and_explicit() -> None:
    payload = yaml.safe_load(Path("tests/fixtures/qa_scenarios.yaml").read_text())
    scenarios = payload["scenarios"]
    assert {item["name"] for item in scenarios} == REQUIRED
    assert len(scenarios) >= 20
    for item in scenarios:
        assert {"route", "outcome", "evidence_ids", "may_resolve"} <= item.keys()
