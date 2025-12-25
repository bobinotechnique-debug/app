"""Smoke test for placeholder API wiring."""

from backend.app.main import create_app
from fastapi.testclient import TestClient


def test_placeholder_endpoint_returns_not_implemented() -> None:
    app = create_app(testing=True)
    client = TestClient(app)

    response = client.get("/api/placeholder")

    assert response.status_code == 501
    assert response.json() == {"detail": "not implemented"}
