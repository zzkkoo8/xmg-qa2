from collections.abc import Iterator

import pytest
from sqlalchemy import text
from sqlalchemy.engine import Engine

from xmg_qa2.infrastructure.db.base import make_engine


@pytest.fixture(scope="session")
def db_engine() -> Iterator[Engine]:
    engine = make_engine()
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    yield engine
    engine.dispose()


@pytest.fixture(autouse=True)
def clean_database(db_engine: Engine) -> Iterator[None]:
    yield
    with db_engine.begin() as connection:
        connection.execute(
            text(
                "TRUNCATE TABLE operation_commit, resume_attempt, human_request, "
                "answer_check, answer_draft, claim_evidence_link, evidence, question_frame, "
                "outbox_event, inbox_event, audit_event, artifact, run, support_task CASCADE"
            )
        )
