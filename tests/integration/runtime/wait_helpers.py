from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy.engine import Engine

from xmg_qa2.domain.task import SupportTask, SupportTaskStatus
from xmg_qa2.infrastructure.checkpoint.postgres import PostgresCheckpointAdapter
from xmg_qa2.infrastructure.db.base import make_session_factory
from xmg_qa2.infrastructure.db.models import RunRow
from xmg_qa2.infrastructure.db.repositories import TaskRepository
from xmg_qa2.runtime.task_service import TaskService


def make_waiting_task(engine: Engine, *, required_fields: dict[str, bool]):
    now = datetime.now(UTC)
    task = SupportTask(
        uuid4(),
        uuid4(),
        "customer",
        None,
        "principal",
        SupportTaskStatus.RUNNING,
        1,
        "support",
        "1",
        "question",
        now,
        now,
    )
    run_id = uuid4()
    factory = make_session_factory(engine)
    with engine.begin() as connection:
        connection.exec_driver_sql(
            "TRUNCATE TABLE resume_attempt, human_request, outbox_event, run, support_task CASCADE"
        )
    with factory.begin() as session:
        TaskRepository(session).create_task(task)
        session.add(
            RunRow(
                id=run_id,
                task_id=task.id,
                status="RUNNING",
                workflow_version="1",
                lease_epoch=1,
                expected_task_version=1,
                started_at=now,
                heartbeat_at=now,
                trace_id="trace",
                created_at=now,
            )
        )
    service = TaskService(
        factory, PostgresCheckpointAdapter("postgresql://xmg_qa2:xmg_qa2@localhost:5432/xmg_qa2")
    )
    request = service.request_input(
        task.id, run_id, "interrupt-1", 1, 1, "Clarify", required_fields
    )
    return service, task, request
