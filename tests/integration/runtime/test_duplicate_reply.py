from xmg_qa2.runtime.task_service import ResumeDecision

from .wait_helpers import make_waiting_task


def test_duplicate_reply_id_has_one_logical_application(db_engine) -> None:  # type: ignore[no-untyped-def]
    service, _, request = make_waiting_task(db_engine, required_fields={"environment": True})
    first = service.accept_reply(
        request.id,
        "same",
        "principal",
        request.interrupt_id,
        request.target_task_version,
        {"environment": "prod"},
    )
    duplicate = service.accept_reply(
        request.id,
        "same",
        "principal",
        request.interrupt_id,
        request.target_task_version,
        {"environment": "prod"},
    )
    assert first.decision is ResumeDecision.QUEUED
    assert duplicate.decision is ResumeDecision.DUPLICATE
    assert duplicate.attempt_id == first.attempt_id
