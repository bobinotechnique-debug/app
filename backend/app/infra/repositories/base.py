"""Base repository protocol placeholders."""

from __future__ import annotations

from typing import Generic, Protocol, TypeVar

T = TypeVar("T")


class Repository(Protocol[T], Generic[T]):
    """Define the minimal repository contract for adapters."""

    def add(self, entity: T) -> None:
        ...

    def get(self, identifier: object) -> T | None:
        ...
