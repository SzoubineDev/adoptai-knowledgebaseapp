"""
Test Fixtures – conftest.py
Project : AdoptAI App Knowledge Base
Author  : Oussama
Stage   : 5 (Testing & Docs)  [B28, B30]

This file is automatically loaded by pytest before any test module runs.
It provides shared fixtures used by both B28 (GET tests) and B30 (DELETE tests).

TESTING STRATEGY — Prisma Mock Pattern
---------------------------------------
Prisma Client Python connects to a live PostgreSQL database and does NOT
support SQLite in-memory mode. Therefore tests use a different strategy:

  1. We create a `MagicMock` that mimics the `Prisma` client interface.
  2. `app.dependency_overrides[get_prisma]` replaces the real Prisma client
     with our mock for the duration of each test.
  3. Individual tests configure mock return values
     (e.g., `mock_db.article.find_unique.return_value = fake_article`)
     to simulate specific database states without touching a real DB.

This approach:
  - Runs in ~milliseconds with zero infrastructure.
  - Is fully deterministic and CI-safe.
  - Tests the FULL request → response pipeline (routing, validation,
    exception handling, serialisation) while isolating the DB layer.

FIXTURE HIERARCHY
-----------------
  mock_prisma      : function-scoped MagicMock mimicking the Prisma client.
  client           : function-scoped TestClient wired to mock_prisma.
  article_factory  : helper that builds consistent fake article dicts/objects.
"""

from datetime import datetime, timezone
from types import SimpleNamespace
from typing import Any, Callable, Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.core.database import get_prisma
from app.main import app


# ---------------------------------------------------------------------------
# Helpers — fake data builders
# ---------------------------------------------------------------------------

def _make_fake_tag(
    id: int = 1,
    name: str = "python",
    slug: str = "python",
) -> SimpleNamespace:
    """
    Build a lightweight fake Tag object that mirrors the Prisma Tag model
    attributes needed by TagResponse (id, name, slug, created_at).
    """
    return SimpleNamespace(
        id=id,
        name=name,
        slug=slug,
        created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )


def _make_fake_category(
    id: int = 1,
    name: str = "SAP",
    slug: str = "sap",
    description: str | None = "SAP ERP articles",
) -> SimpleNamespace:
    """
    Build a lightweight fake Category object that mirrors Prisma Category model
    attributes needed by CategoryResponse (id, name, slug, description, timestamps).
    """
    return SimpleNamespace(
        id=id,
        name=name,
        slug=slug,
        description=description,
        created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        updated_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )


def make_fake_article(
    id: int = 1,
    title: str = "Test Article",
    slug: str = "test-article",
    content: str = "Test article content for the AdoptAI knowledge base.",
    status: str = "published",
    type_hebergement: str | None = None,
    category_id: int | None = None,
    category: Any | None = None,
    tags: list | None = None,
) -> SimpleNamespace:
    """
    Build a lightweight fake Article object that mirrors the fields expected
    by ArticleResponse.model_validate() (from_attributes=True).

    Prisma model field names use camelCase internally; our ArticleResponse
    schema maps from the ORM attribute names. Since we use SimpleNamespace
    and model_validate with from_attributes=True, field names must match
    the Pydantic schema's expected aliases / field names.
    """
    return SimpleNamespace(
        id=id,
        title=title,
        slug=slug,
        content=content,
        status=status,
        type_hebergement=type_hebergement,
        category_id=category_id,
        category=category,
        tags=tags if tags is not None else [],
        created_at=datetime(2026, 6, 1, 12, 0, 0, tzinfo=timezone.utc),
        updated_at=datetime(2026, 6, 1, 12, 0, 0, tzinfo=timezone.utc),
    )


# ---------------------------------------------------------------------------
# mock_prisma fixture — replaces the live Prisma client
# ---------------------------------------------------------------------------

@pytest.fixture(scope="function")
def mock_prisma() -> MagicMock:
    """
    Returns a MagicMock that mimics the Prisma client's async API surface.

    The mock automatically creates child mocks for any attribute access,
    so `mock_db.article.find_unique`, `mock_db.article.delete`, etc. are
    all valid AsyncMock targets that tests can configure freely.

    Usage in a test:
        def test_something(client, mock_prisma):
            mock_prisma.article.find_unique = AsyncMock(
                return_value=make_fake_article(id=1)
            )
            response = client.get("/api/v1/articles/1")
            assert response.status_code == 200
    """
    mock = MagicMock()

    # Pre-configure the most common async methods so tests only need to
    # set `return_value` rather than convert to AsyncMock themselves.
    mock.article.find_unique = AsyncMock(return_value=None)
    mock.article.find_first = AsyncMock(return_value=None)
    mock.article.find_many = AsyncMock(return_value=[])
    mock.article.create = AsyncMock(return_value=None)
    mock.article.update = AsyncMock(return_value=None)
    mock.article.delete = AsyncMock(return_value=None)
    mock.article.count = AsyncMock(return_value=0)

    return mock


# ---------------------------------------------------------------------------
# client fixture — TestClient wired to mock_prisma
# ---------------------------------------------------------------------------

@pytest.fixture(scope="function")
def client(mock_prisma: MagicMock) -> Generator[TestClient, None, None]:
    """
    Yield a synchronous `TestClient` that routes all Prisma calls through
    `mock_prisma` instead of a live database.

    FastAPI's `dependency_overrides` is the official mechanism:
      - `get_prisma` is replaced by an async generator that yields mock_prisma.
      - After the test, overrides are cleared to prevent cross-test leakage.
    """
    async def override_get_prisma():
        yield mock_prisma

    app.dependency_overrides[get_prisma] = override_get_prisma

    with TestClient(app, raise_server_exceptions=True) as test_client:
        yield test_client

    app.dependency_overrides.clear()
