from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy.engine import Engine

from xmg_qa2.domain.task import RunStatus, SupportTask, SupportTaskStatus
from xmg_qa2.infrastructure.db.base import make_session_factory
from xmg_qa2.infrastructure.db.models import RunRow
from xmg_qa2.infrastructure.db.repositories import TaskRepository


def test_operation_id_is_idempotent_per_task(db_engine: Engine) -> None:
    factory = make_session_factory(db_engine)
    now = datetime.now(UTC)
    task = SupportTask(
        uuid4(), uuid4(), "customer", None, "principal", SupportTaskStatus.RUNNING, 1,
        "support", "1", "question", now, now,
    )
    run_id = uuid4()
    with factory.begin() as session:
        repository = TaskRepository(session)
        repository.create_task(task)
        session.add(
            RunRow(
                id=run_id, task_id=task.id, status=RunStatus.RUNNING.value,
                workflow_version="1", lease_epoch=1, expected_task_version=1,
                started_at=now, heartbeat_at=now, trace_id="trace", created_at=now,
            )
        )

    arguments = {
        "task_id": task.id,
        "run_id": run_id,
        "operation_id": "same-operation",
        "lease_epoch": 1,
        "task_version_before": 1,
        "task_version_after": 2,
        "operation_type": "TEST",
        "result_digest": "digest",
    }
    with factory.begin() as first:
        assert TaskRepository(first).commit_operation(**arguments)
    with factory() as duplicate:
        assert not TaskRepository(duplicate).commit_operation(**arguments)
