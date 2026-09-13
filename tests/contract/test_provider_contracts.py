from dataclasses import asdict

from xmg_qa2.harness.contracts.common import (
    CapabilityDescriptor,
    CapabilityEffect,
    InvocationContext,
)
from xmg_qa2.harness.contracts.knowledge import EvidenceCandidate
from xmg_qa2.harness.contracts.model import ModelUsage


def test_contract_dtos_are_project_owned_and_serializable() -> None:
    descriptor = CapabilityDescriptor(
        capability_id="knowledge.search",
        provider_kind="KNOWLEDGE",
        provider_id="fake",
        version="1",
        schema_hash="schema-1",
        effect=CapabilityEffect.READ_ONLY,
        enabled=True,
        timeout_seconds=10,
        metadata={"fixture": True},
    )
    context = InvocationContext(
        task_id="task",
        case_id="case",
        customer_id="customer",
        project_id=None,
        principal_id="principal",
        run_id="run",
        operation_id="operation",
        trace_id="trace",
    )
    assert asdict(descriptor)["capability_id"] == "knowledge.search"
    assert asdict(context)["project_id"] is None


def test_unknown_model_usage_remains_none() -> None:
    usage = ModelUsage(input_tokens=None, output_tokens=None, cost=None)
    assert usage.input_tokens is None
    assert usage.output_tokens is None
    assert usage.cost is None


def test_non_document_evidence_does_not_require_document_identifiers() -> None:
    candidate = EvidenceCandidate(
        source_name="health-api",
        source_locator=None,
        excerpt="service is healthy",
        collected_at="2026-09-14T00:00:00Z",
        product=None,
        product_version=None,
        retrieval_score=None,
        provenance={"request_id": "req-1"},
    )
    assert candidate.source_locator is None
