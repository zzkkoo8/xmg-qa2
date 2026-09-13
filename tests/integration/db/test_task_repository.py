from datetime import UTC, datetime
from uuid import uuid4

import pytest
from sqlalchemy.engine import Engine

from xmg_qa2.domain.errors import StaleStateVersion
from xmg_qa2.domain.task import SupportTask, SupportTaskStatus
from xmg_qa2.infrastructure.db.base import make_session_factory
from xmg_qa2.infrastructure.db.repositories import TaskRepository


def make_task() -> SupportTask:
    now = datetime.now(UTC)
    return SupportTask(
        uuid4(), uuid4(), "customer", None, "principal", SupportTaskStatus.NEW, 1,
        "support", "1", "question", now, now,
    )


def test_concurrent_expected_version_allows_exactly_one_transition(db_engine: Engine) -> None:
    factory = make_session_factory(db_engine)
    task = make_task()
    with factory.begin() as setup:
        TaskRepository(setup).create_task(task)

    first = factory()
    second = factory()
    try:
        TaskRepository(first).transition_task(task.id, 1, SupportTaskStatus.RUNNING.value)
        first.commit()
        with pytest.raises(StaleStateVersion):
            TaskRepository(second).transition_task(task.id, 1, SupportTaskStatus.CANCELLED.value)
        second.rollback()
    finally:
        first.close()
        second.close()

    with factory() as check:
        row = TaskRepository(check).get_task(task.id)
        assert row is not None
        assert row.status == SupportTaskStatus.RUNNING.value
        assert row.state_version == 2
