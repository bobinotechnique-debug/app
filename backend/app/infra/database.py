"""Database session management placeholders."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


class DatabaseSessionManager:
    """Manage database sessions without enforcing domain rules."""

    def __init__(self, database_url: str | None) -> None:
        self.database_url = database_url
        self._engine: Engine | None = create_engine(database_url) if database_url else None
        self._SessionLocal = sessionmaker(bind=self._engine) if self._engine else None

    @contextmanager
    def session_scope(self) -> Generator[Session | None, None, None]:
        """Provide a database session scope when configured."""

        if self._SessionLocal is None:
            yield None
            return

        session = self._SessionLocal()
        try:
            yield session
        finally:
            session.close()
