from fastapi.testclient import TestClient

from app.main import app


def test_dashboard_summary() -> None:
    client = TestClient(app)

    response = client.get("/api/dashboard/summary")

    assert response.status_code == 200
    body = response.json()
    assert body["service_status"] == "ok"
    assert body["automation_boundary"] == "L0-L1"

