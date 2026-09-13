from fastapi.testclient import TestClient

from tests.integration.api.conftest import auth_header


def test_case_acl_is_separate_from_authentication(api_client: TestClient) -> None:
    alice = auth_header(api_client)
    task_id = api_client.post(
        "/api/v1/tasks", headers=alice, json={"question": "q", "customer_id": "c"}
    ).json()["task_id"]
    bob = auth_header(api_client, "bob", "bob-pass")
    assert api_client.get(f"/api/v1/tasks/{task_id}", headers=bob).status_code == 403
