from fastapi.testclient import TestClient

from app.main import app


def test_kill_switch_defaults_refund_paused() -> None:
    client = TestClient(app)

    response = client.get("/api/risk/kill-switches")

    assert response.status_code == 200
    body = response.json()
    assert body["refund_pause"] is True
    assert body["global_pause"] is False


def test_kill_switch_can_update_global_pause() -> None:
    client = TestClient(app)

    response = client.post(
        "/api/risk/kill-switches",
        json={"store_id": "test-store", "global_pause": True, "updated_by": "qa"},
    )

    assert response.status_code == 200
    assert response.json()["global_pause"] is True

