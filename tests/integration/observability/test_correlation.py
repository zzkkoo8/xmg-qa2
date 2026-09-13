from xmg_qa2.observability.audit import SafeAuditEvent
from xmg_qa2.observability.logging import correlation, current_correlation


def test_runtime_provider_and_api_fields_share_correlation() -> None:
    with correlation(task_id="task", case_id="case", run_id="run", trace_id="trace"):
        values = current_correlation()
        event = SafeAuditEvent(
            **values,
            operation_id="operation",
            workflow="support",
            workflow_version="1",
            node="retrieve_evidence",
            provider_id="fake",
            capability_id="knowledge.search",
            latency_ms=12.5,
            retry_count=0,
            evidence_ids=("evidence-1",),
            outcome="COMPLETE",
            reason_code="OK",
        )
    assert event.safe_metadata()["trace_id"] == "trace"
    assert event.safe_metadata()["evidence_ids"] == ("evidence-1",)
