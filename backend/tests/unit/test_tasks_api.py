from fastapi.testclient import TestClient

from app.main import app


def test_exception_tasks_expose_role_and_next_action() -> None:
    client = TestClient(app)

    response = client.get("/api/tasks/exceptions")

    assert response.status_code == 200
    items = response.json()["items"]
    assert len(items) >= 1
    assert {"owner_role", "next_action", "severity"}.issubset(items[0].keys())

