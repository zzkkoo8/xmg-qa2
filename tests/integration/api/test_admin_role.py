from fastapi.testclient import TestClient

from tests.integration.api.conftest import auth_header


def test_admin_ping_requires_admin_role(api_client: TestClient) -> None:
    assert api_client.get("/api/v1/admin/ping", headers=auth_header(api_client)).status_code == 403
    assert api_client.get(
        "/api/v1/admin/ping", headers=auth_header(api_client, "admin", "admin-pass")
    ).json() == {"ok": True}
