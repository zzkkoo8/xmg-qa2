from sqlalchemy import inspect
from sqlalchemy.engine import Engine


def test_initial_migration_creates_business_state_tables(db_engine: Engine) -> None:
    tables = set(inspect(db_engine).get_table_names())
    assert {
        "support_task",
        "run",
        "human_request",
        "resume_attempt",
        "evidence",
        "answer_draft",
        "answer_check",
        "operation_commit",
        "outbox_event",
        "audit_event",
    } <= tables
