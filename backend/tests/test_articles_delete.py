"""
B30 - Backend Tests: Article Deletion
Project : AdoptAI App Knowledge Base
Author  : Oussama
Stage   : 5 (Testing & Docs)

Tests the DELETE /api/v1/articles/{id} endpoint (B13) using FastAPI
TestClient + Prisma mock fixtures from conftest.py.

TESTING STRATEGY
----------------
The Prisma client is replaced with a MagicMock via `app.dependency_overrides`
(see conftest.py). Each test configures two mock behaviours:

  1. `mock_prisma.article.find_unique` — simulates the existence check
     (`article_repository.get()` before deletion).
  2. `mock_prisma.article.delete`      — simulates the actual delete call.

Setting `find_unique.return_value = None` simulates a missing article (→ 404).
Setting `find_unique.return_value = make_fake_article(...)` simulates a hit (→ 204).

This decouples tests from any real database, keeps them fast (~ms), and
proves the full pipeline: routing → existence check → delete → 204 / 404.

TEST COVERAGE — B30
-------------------
Happy path (HTTP 204):
  ✅ 204 No Content for an existing article
  ✅ Response body is strictly empty (RFC 9110 §15.3.5)
  ✅ `article.delete` is called exactly once after a successful find
  ✅ Deleting a DRAFT article also returns 204
  ✅ Deleting an ARCHIVED article also returns 204

Error paths (HTTP 404):
  ✅ 404 for a non-existent article id
  ✅ Standard error envelope {"error": {"code", "message", "status"}}
  ✅ Error code is "ARTICLE_NOT_FOUND"
  ✅ Error status in body equals 404
  ✅ Error message contains the requested id
  ✅ `article.delete` is NOT called when the article is not found
  ✅ Second delete on the same id returns 404 (idempotency)

Input validation (HTTP 422):
  ✅ 422 for id = 0   (ge=1 constraint)
  ✅ 422 for id = -1  (ge=1 constraint)
  ✅ 422 for non-integer id
"""

from unittest.mock import AsyncMock, call

import pytest
from fastapi.testclient import TestClient

from tests.conftest import make_fake_article


# ===========================================================================
# DELETE /articles/{id} — 204 Happy path
# ===========================================================================

class TestDeleteArticleSuccess:
    """Tests for successful article deletion (HTTP 204 No Content)."""

    @pytest.mark.integration
    def test_returns_204_for_existing_article(
        self, client: TestClient, mock_prisma
    ):
        """
        GIVEN  the repository finds the article (find_unique returns a fake article)
        WHEN   DELETE /api/v1/articles/1 is called
        THEN   the response status code is 204 No Content
        """
        mock_prisma.article.find_unique = AsyncMock(
            return_value=make_fake_article(id=1)
        )
        mock_prisma.article.delete = AsyncMock(return_value=None)

        response = client.delete("/api/v1/articles/1")

        assert response.status_code == 204

    @pytest.mark.integration
    def test_response_body_is_strictly_empty(
        self, client: TestClient, mock_prisma
    ):
        """
        GIVEN  a successful deletion
        WHEN   DELETE /api/v1/articles/1 is called
        THEN   the raw response content is b"" (RFC 9110 §15.3.5 — no body on 204)
        """
        mock_prisma.article.find_unique = AsyncMock(
            return_value=make_fake_article(id=1)
        )
        mock_prisma.article.delete = AsyncMock(return_value=None)

        response = client.delete("/api/v1/articles/1")

        assert response.content == b""

    @pytest.mark.integration
    def test_delete_is_called_exactly_once(
        self, client: TestClient, mock_prisma
    ):
        """
        GIVEN  a successful deletion
        WHEN   DELETE /api/v1/articles/5 is called
        THEN   `article.delete` is called exactly one time (not zero, not twice)
        """
        mock_prisma.article.find_unique = AsyncMock(
            return_value=make_fake_article(id=5, slug="article-five")
        )
        mock_prisma.article.delete = AsyncMock(return_value=None)

        client.delete("/api/v1/articles/5")

        mock_prisma.article.delete.assert_called_once()

    @pytest.mark.integration
    def test_delete_draft_article_returns_204(
        self, client: TestClient, mock_prisma
    ):
        """
        GIVEN  a DRAFT article exists
        WHEN   DELETE /api/v1/articles/1 is called
        THEN   status 204 (lifecycle state does not block deletion)
        """
        mock_prisma.article.find_unique = AsyncMock(
            return_value=make_fake_article(id=1, status="draft", slug="draft-del-test")
        )
        mock_prisma.article.delete = AsyncMock(return_value=None)

        response = client.delete("/api/v1/articles/1")

        assert response.status_code == 204

    @pytest.mark.integration
    def test_delete_archived_article_returns_204(
        self, client: TestClient, mock_prisma
    ):
        """
        GIVEN  an ARCHIVED article exists
        WHEN   DELETE /api/v1/articles/1 is called
        THEN   status 204 (archived articles can be permanently removed)
        """
        mock_prisma.article.find_unique = AsyncMock(
            return_value=make_fake_article(id=1, status="archived", slug="archived-del-test")
        )
        mock_prisma.article.delete = AsyncMock(return_value=None)

        response = client.delete("/api/v1/articles/1")

        assert response.status_code == 204


# ===========================================================================
# DELETE /articles/{id} — 404 Error paths
# ===========================================================================

class TestDeleteArticleNotFound:
    """Tests for the 404 Not Found error path on DELETE /api/v1/articles/{id}."""

    @pytest.mark.integration
    def test_returns_404_when_article_does_not_exist(
        self, client: TestClient, mock_prisma
    ):
        """
        GIVEN  find_unique returns None (article missing)
        WHEN   DELETE /api/v1/articles/99999 is called
        THEN   the response status code is 404 Not Found
        """
        mock_prisma.article.find_unique = AsyncMock(return_value=None)

        response = client.delete("/api/v1/articles/99999")

        assert response.status_code == 404

    @pytest.mark.integration
    def test_404_response_has_standard_error_envelope(
        self, client: TestClient, mock_prisma
    ):
        """
        GIVEN  the article does not exist
        WHEN   DELETE /api/v1/articles/99999 is called
        THEN   body is {"error": {"code": ..., "message": ..., "status": ...}}
        """
        mock_prisma.article.find_unique = AsyncMock(return_value=None)
        data = client.delete("/api/v1/articles/99999").json()

        assert "error" in data
        assert all(k in data["error"] for k in ("code", "message", "status"))

    @pytest.mark.integration
    def test_404_error_code_is_article_not_found(
        self, client: TestClient, mock_prisma
    ):
        """
        GIVEN  the article does not exist
        WHEN   DELETE /api/v1/articles/99999 is called
        THEN   the error code is exactly "ARTICLE_NOT_FOUND"
        """
        mock_prisma.article.find_unique = AsyncMock(return_value=None)
        data = client.delete("/api/v1/articles/99999").json()

        assert data["error"]["code"] == "ARTICLE_NOT_FOUND"

    @pytest.mark.integration
    def test_404_error_status_equals_404(
        self, client: TestClient, mock_prisma
    ):
        """
        GIVEN  the article does not exist
        WHEN   DELETE /api/v1/articles/99999 is called
        THEN   the "status" field inside the error envelope equals 404
        """
        mock_prisma.article.find_unique = AsyncMock(return_value=None)
        data = client.delete("/api/v1/articles/99999").json()

        assert data["error"]["status"] == 404

    @pytest.mark.integration
    def test_404_error_message_contains_requested_id(
        self, client: TestClient, mock_prisma
    ):
        """
        GIVEN  no article with id 55555 exists
        WHEN   DELETE /api/v1/articles/55555 is called
        THEN   the error message contains "55555"
        """
        mock_prisma.article.find_unique = AsyncMock(return_value=None)
        data = client.delete("/api/v1/articles/55555").json()

        assert "55555" in data["error"]["message"]

    @pytest.mark.integration
    def test_delete_is_not_called_when_article_not_found(
        self, client: TestClient, mock_prisma
    ):
        """
        GIVEN  the article does not exist (find_unique returns None)
        WHEN   DELETE /api/v1/articles/99999 is called
        THEN   `article.delete` is NEVER called
               (the handler raises 404 before reaching the delete call)
        """
        mock_prisma.article.find_unique = AsyncMock(return_value=None)
        mock_prisma.article.delete = AsyncMock(return_value=None)

        client.delete("/api/v1/articles/99999")

        mock_prisma.article.delete.assert_not_called()

    @pytest.mark.integration
    def test_double_delete_second_call_returns_404(
        self, client: TestClient, mock_prisma
    ):
        """
        GIVEN  the first DELETE succeeds (article existed)
        AND    the second DELETE targets the same id (now gone → find_unique = None)
        WHEN   DELETE /api/v1/articles/{id} is called twice
        THEN   the first call returns 204, the second returns 404
               (idempotency: repeated deletes behave correctly)
        """
        article = make_fake_article(id=10, slug="double-delete-test")

        # First call: article exists.
        mock_prisma.article.find_unique = AsyncMock(return_value=article)
        mock_prisma.article.delete = AsyncMock(return_value=None)
        first = client.delete("/api/v1/articles/10")
        assert first.status_code == 204

        # Second call: article is gone.
        mock_prisma.article.find_unique = AsyncMock(return_value=None)
        second = client.delete("/api/v1/articles/10")
        assert second.status_code == 404


# ===========================================================================
# DELETE /articles/{id} — 422 Input validation
# ===========================================================================

class TestDeleteArticleInputValidation:
    """Tests for FastAPI path parameter validation on DELETE."""

    @pytest.mark.integration
    def test_id_zero_returns_422(self, client: TestClient, mock_prisma):
        """id=0 violates Path(..., ge=1) → 422 before the handler runs."""
        assert client.delete("/api/v1/articles/0").status_code == 422

    @pytest.mark.integration
    def test_negative_id_returns_422(self, client: TestClient, mock_prisma):
        """id=-1 violates ge=1 → 422."""
        assert client.delete("/api/v1/articles/-1").status_code == 422

    @pytest.mark.integration
    def test_string_id_returns_422(self, client: TestClient, mock_prisma):
        """id='invalid' cannot be coerced to int → 422."""
        assert client.delete("/api/v1/articles/invalid").status_code == 422
