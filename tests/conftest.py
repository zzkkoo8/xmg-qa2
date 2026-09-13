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
