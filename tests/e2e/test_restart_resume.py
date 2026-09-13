from tests.integration.runtime.wait_helpers import make_waiting_task
from xmg_qa2.infrastructure.checkpoint.postgres import PostgresCheckpointAdapter
from xmg_qa2.infrastructure.db.base import make_session_factory
from xmg_qa2.runtime.task_service import TaskService


def test_service_restart_resumes_same_task(db_engine) -> None:  # type: ignore[no-untyped-def]
    _, task, request = make_waiting_task(db_engine, required_fields={"environment": True})
    restarted = TaskService(
        make_session_factory(db_engine),
        PostgresCheckpointAdapter("postgresql://xmg_qa2:xmg_qa2@localhost:5432/xmg_qa2"),
    )
    assert restarted.task_id_for_request(request.id) == task.id
