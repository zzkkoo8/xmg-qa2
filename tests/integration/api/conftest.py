from collections.abc import Iterator
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.engine import Engine

from xmg_qa2.api.app import create_app
from xmg_qa2.api.deps import UserRecord
from xmg_qa2.infrastructure.auth.passwords import hash_password
from xmg_qa2.infrastructure.db.base import make_session_factory


@pytest.fixture()
def api_client(db_engine: Engine) -> Iterator[TestClient]:
    with db_engine.begin() as connection:
        connection.exec_driver_sql("TRUNCATE TABLE outbox_event, support_task CASCADE")
    users = [
        UserRecord("user-1", "alice", hash_password("alice-pass")),
        UserRecord("user-2", "bob", hash_password("bob-pass")),
        UserRecord("admin-1", "admin", hash_password("admin-pass"), ("admin",)),
    ]
    with TestClient(
        create_app(make_session_factory(db_engine), users, f"test-secret-{uuid4()}")
    ) as client:
        yield client


def auth_header(
    client: TestClient, username: str = "alice", password: str = "alice-pass"
) -> dict[str, str]:
    response = client.post("/api/v1/auth/login", json={"username": username, "password": password})
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}
