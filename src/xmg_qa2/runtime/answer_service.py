"""Deterministic evidence and safety checks for answer drafts."""

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class AnswerMaterial:
    answer_kind: str
    required_subquestions: set[str]
    covered_subquestions: set[str]
    product_version_claim: str | None = None
    cited_evidence_ids: set[str] = field(default_factory=set)
    accessible_evidence: dict[str, str | None] = field(default_factory=dict)
    claims_executed_action: bool = False
    executed_action_evidence: bool = False
    customer_write_represented_as_executed: bool = False


@dataclass(frozen=True, slots=True)
class AnswerVerification:
    passed: bool
    issues: tuple[str, ...]


class AnswerVerifier:
    def check(self, material: AnswerMaterial) -> AnswerVerification:
        issues: list[str] = []
        uncovered = material.required_subquestions - material.covered_subquestions
        if material.answer_kind == "COMPLETE" and uncovered:
            issues.append("UNCOVERED_REQUIRED_SUBQUESTION")
        if material.product_version_claim is not None and not any(
            version == material.product_version_claim
            for version in material.accessible_evidence.values()
        ):
            issues.append("NO_APPLICABLE_PRODUCT_VERSION_EVIDENCE")
        if not material.cited_evidence_ids <= material.accessible_evidence.keys():
            issues.append("UNKNOWN_OR_INACCESSIBLE_CITATION")
        if material.claims_executed_action and not material.executed_action_evidence:
            issues.append("UNPROVEN_EXECUTED_ACTION")
        if material.customer_write_represented_as_executed:
            issues.append("CUSTOMER_WRITE_REPRESENTED_AS_EXECUTED")
        return AnswerVerification(not issues, tuple(issues))
