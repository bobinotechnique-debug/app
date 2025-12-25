"""Smoke tests for health endpoints."""

from backend.app.main import create_app
from fastapi.testclient import TestClient


def test_live_health_returns_ok() -> None:
    app = create_app(testing=True)
    client = TestClient(app)

    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ready_health_returns_ok_in_testing() -> None:
    app = create_app(testing=True)
    client = TestClient(app)

    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ready_health_runs_dependency_check_when_not_testing() -> None:
    invoked = {"value": False}

    def dependency_check() -> None:
        invoked["value"] = True

    app = create_app(dependency_check=dependency_check, testing=False)
    client = TestClient(app)

    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert invoked["value"] is True


def test_ready_health_allows_none_dependency_hook() -> None:
    app = create_app(testing=False)
    client = TestClient(app)

    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

