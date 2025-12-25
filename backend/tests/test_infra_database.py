"""Database session manager hardening tests."""

from __future__ import annotations

from backend.app.infra.database import DatabaseSessionManager


def test_session_scope_yields_none_when_unconfigured() -> None:
    manager = DatabaseSessionManager(database_url=None)

    with manager.session_scope() as session:
        assert session is None

    manager.dispose()


def test_configured_property_matches_url_presence() -> None:
    manager_without_url = DatabaseSessionManager(database_url=None)
    assert manager_without_url.configured is False

    manager_with_url = DatabaseSessionManager(database_url="sqlite:///:memory:")
    assert manager_with_url.configured is True

    manager_with_url.dispose()
