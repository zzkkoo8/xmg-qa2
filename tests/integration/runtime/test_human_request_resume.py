from xmg_qa2.runtime.task_service import ResumeDecision

from .wait_helpers import make_waiting_task


def test_complete_reply_is_applied_only_after_workflow_consumes(db_engine) -> None:  # type: ignore[no-untyped-def]
    service, task, request = make_waiting_task(db_engine, required_fields={"environment": True})
    accepted = service.accept_reply(
        request.id,
        "reply-1",
        "principal",
        request.interrupt_id,
        request.target_task_version,
        {"environment": "prod"},
    )
    assert accepted.decision is ResumeDecision.QUEUED
    assert service.resume_status(accepted.attempt_id) == "QUEUED"
    service.mark_resume_consumed(accepted.attempt_id)
    assert service.resume_status(accepted.attempt_id) == "APPLIED"
    assert service.task_id_for_request(request.id) == task.id


def test_partial_reply_remains_waiting_for_missing_fields(db_engine) -> None:  # type: ignore[no-untyped-def]
    service, _, request = make_waiting_task(
        db_engine, required_fields={"environment": True, "version": True}
    )
    result = service.accept_reply(
        request.id,
        "reply-partial",
        "principal",
        request.interrupt_id,
        request.target_task_version,
        {"environment": "prod"},
    )
    assert result.decision is ResumeDecision.PARTIAL
    assert result.missing_fields == ("version",)
    assert service.request_status(request.id) == "PENDING"
