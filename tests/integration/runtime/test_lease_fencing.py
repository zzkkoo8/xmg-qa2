from datetime import UTC, datetime
from uuid import uuid4

import pytest

from xmg_qa2.domain.errors import StaleStateVersion
from xmg_qa2.infrastructure.db.base import make_engine, make_session_factory
from xmg_qa2.infrastructure.db.models import RunRow
from xmg_qa2.infrastructure.db.repositories import TaskRepository


def test_old_worker_cannot_renew_after_lease_epoch_changes() -> None:
    engine = make_engine()
    factory = make_session_factory(engine)
    now = datetime.now(UTC)
    run_id = uuid4()
    task_id = uuid4()
    with engine.begin() as connection:
        connection.exec_driver_sql("TRUNCATE TABLE run, support_task CASCADE")
        connection.exec_driver_sql(
            "INSERT INTO support_task(id,case_id,customer_id,created_by_principal,status,state_version,workflow_name,workflow_version,question_text,created_at,updated_at) VALUES (%s,%s,'c','p','RUNNING',1,'support','1','q',now(),now())",
            (task_id, uuid4()),
        )
    with factory.begin() as session:
        session.add(RunRow(id=run_id, task_id=task_id, status="RUNNING", workflow_version="1", lease_epoch=1, expected_task_version=1, started_at=now, heartbeat_at=now, trace_id="trace", created_at=now))
    with factory.begin() as current:
        assert TaskRepository(current).acquire_or_renew_lease(run_id, 1) == 2
    with factory() as stale:
        with pytest.raises(StaleStateVersion):
            TaskRepository(stale).acquire_or_renew_lease(run_id, 1)
        stale.rollback()
    engine.dispose()
