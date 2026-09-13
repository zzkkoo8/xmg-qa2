from fastapi.testclient import TestClient
from sqlalchemy import func, select

from tests.integration.api.conftest import auth_header
from xmg_qa2.infrastructure.db.models import OutboxEventRow, SupportTaskRow


def test_create_task_persists_business_state_and_outbox(api_client: TestClient) -> None:
    headers = auth_header(api_client)
    response = api_client.post(
        "/api/v1/tasks",
        headers=headers,
        json={"question": "Why unavailable?", "customer_id": "customer"},
    )
    assert response.status_code == 202
    task_id = response.json()["task_id"]
    sessions = api_client.app.state.sessions
    with sessions() as session:
        assert session.get(SupportTaskRow, task_id) is not None
        assert session.scalar(select(func.count()).select_from(OutboxEventRow)) == 1
    assert api_client.get(f"/api/v1/tasks/{task_id}", headers=headers).status_code == 200


def test_login_rejects_invalid_credentials(api_client: TestClient) -> None:
    assert (
        api_client.post(
            "/api/v1/auth/login", json={"username": "alice", "password": "wrong"}
        ).status_code
        == 401
    )
