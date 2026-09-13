from xmg_qa2.runtime.answer_service import AnswerMaterial, AnswerVerifier


def test_complete_answer_rejects_uncovered_critical_subquestion() -> None:
    result = AnswerVerifier().check(
        AnswerMaterial(answer_kind="COMPLETE", required_subquestions={"critical"}, covered_subquestions=set())
    )
    assert "UNCOVERED_REQUIRED_SUBQUESTION" in result.issues


def test_product_claim_requires_applicable_evidence_and_known_citation() -> None:
    result = AnswerVerifier().check(
        AnswerMaterial(
            answer_kind="COMPLETE",
            required_subquestions=set(),
            covered_subquestions=set(),
            product_version_claim="2.0",
            cited_evidence_ids={"unknown"},
            accessible_evidence={},
        )
    )
    assert "NO_APPLICABLE_PRODUCT_VERSION_EVIDENCE" in result.issues
    assert "UNKNOWN_OR_INACCESSIBLE_CITATION" in result.issues


def test_recommended_write_cannot_be_reported_as_executed() -> None:
    result = AnswerVerifier().check(
        AnswerMaterial(
            answer_kind="COMPLETE",
            required_subquestions=set(),
            covered_subquestions=set(),
            claims_executed_action=True,
            executed_action_evidence=False,
            customer_write_represented_as_executed=True,
        )
    )
    assert "UNPROVEN_EXECUTED_ACTION" in result.issues
    assert "CUSTOMER_WRITE_REPRESENTED_AS_EXECUTED" in result.issues
