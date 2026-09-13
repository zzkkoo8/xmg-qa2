from xmg_qa2.runtime.task_service import ResumeDecision

from .wait_helpers import make_waiting_task


def test_stale_interrupt_or_version_is_rejected_and_audited(db_engine) -> None:  # type: ignore[no-untyped-def]
    service, _, request = make_waiting_task(db_engine, required_fields={"environment": True})
    result = service.accept_reply(
        request.id,
        "stale",
        "principal",
        "old-interrupt",
        request.target_task_version - 1,
        {"environment": "prod"},
    )
    assert result.decision is ResumeDecision.REJECTED_STALE
    assert service.resume_status(result.attempt_id) == "REJECTED"
