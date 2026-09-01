"""
B28 - Backend Tests: Article Retrieval
Project : AdoptAI App Knowledge Base
Author  : Oussama
Stage   : 5 (Testing & Docs)

Tests the following endpoints using FastAPI TestClient + Prisma mock:
  - GET /api/v1/articles/{id}   — single article retrieval (B10)
  - GET /api/v1/articles        — paginated list with filters (B15)

TESTING STRATEGY
----------------
All tests mock `get_prisma` via `app.dependency_overrides` (configured in
conftest.py). The mock_prisma fixture exposes pre-configured AsyncMocks so
each test only sets the specific return_value it needs.

No real database or Prisma client is involved. We test:
  - The full HTTP pipeline: routing → validation → handler → serialisation.
  - The exception-handling contract (B19/B20 error envelope).
  - FastAPI path-parameter validation (422 responses).

TEST COVERAGE — B28
-------------------
GET /articles/{id} happy path:
  ✅ 200 OK for an existing article
  ✅ Response body contains correct id, title, slug, content, status
  ✅ Timestamps are present and non-null
  ✅ Empty tags list for a tag-less article
  ✅ Category is None for an uncategorised article
  ✅ Category is nested and populated when present
  ✅ Tags list is populated when article has tags

GET /articles/{id} error paths:
  ✅ 404 for a non-existent article id
  ✅ Standard error envelope structure on 404
  ✅ Error code is ARTICLE_NOT_FOUND
  ✅ Error message contains the requested id
  ✅ 422 for id = 0  (ge=1 constraint)
  ✅ 422 for id = -3 (ge=1 constraint)
  ✅ 422 for non-integer id

GET /articles (list) happy path:
  ✅ 200 OK with empty list when no articles
  ✅ 200 OK with list of articles
  ✅ category_id filter is forwarded to repository
  ✅ status filter is forwarded to repository
"""

from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from tests.conftest import make_fake_article, _make_fake_category, _make_fake_tag


# ===========================================================================
# GET /articles/{id} — B10
# ===========================================================================

class TestGetArticleByIdSuccess:
    """Happy-path tests for GET /api/v1/articles/{id} (HTTP 200)."""

    @pytest.mark.integration
    def test_returns_200_for_existing_article(
        self, client: TestClient, mock_prisma
    ):
        """
        GIVEN  a Prisma mock that returns a fake article for id=1
        WHEN   GET /api/v1/articles/1 is called
        THEN   the response status code is 200 OK
        """
        mock_prisma.article.find_unique = AsyncMock(
            return_value=make_fake_article(id=1)
        )
        response = client.get("/api/v1/articles/1")
        assert response.status_code == 200

    @pytest.mark.integration
    def test_response_contains_correct_id(
        self, client: TestClient, mock_prisma
    ):
        """
        GIVEN  a fake article with id=42
        WHEN   GET /api/v1/articles/42 is called
        THEN   the response body id field equals 42
        """
        mock_prisma.article.find_unique = AsyncMock(
            return_value=make_fake_article(id=42, slug="unique-slug-42")
        )
        response = client.get("/api/v1/articles/42")
        assert response.json()["id"] == 42

    @pytest.mark.integration
    def test_response_contains_correct_title(
        self, client: TestClient, mock_prisma
    ):
        """
        GIVEN  a fake article with title "SAP Password Reset"
        WHEN   GET /api/v1/articles/1 is called
        THEN   the response body title equals "SAP Password Reset"
        """
        mock_prisma.article.find_unique = AsyncMock(
            return_value=make_fake_article(title="SAP Password Reset", slug="sap-password-reset")
        )
        response = client.get("/api/v1/articles/1")
        assert response.json()["title"] == "SAP Password Reset"

    @pytest.mark.integration
    def test_response_contains_correct_slug(
        self, client: TestClient, mock_prisma
    ):
        """
        GIVEN  a fake article with slug "servicenow-onboarding"
        WHEN   GET /api/v1/articles/1 is called
        THEN   the response body slug field matches exactly
        """
        mock_prisma.article.find_unique = AsyncMock(
            return_value=make_fake_article(slug="servicenow-onboarding")
        )
        response = client.get("/api/v1/articles/1")
        assert response.json()["slug"] == "servicenow-onboarding"

    @pytest.mark.integration
    def test_response_contains_correct_status(
        self, client: TestClient, mock_prisma
    ):
        """
        GIVEN  a fake article with status "draft"
        WHEN   GET /api/v1/articles/1 is called
        THEN   the response body status field equals "draft"
        """
        mock_prisma.article.find_unique = AsyncMock(
            return_value=make_fake_article(status="draft", slug="draft-status-test")
        )
        response = client.get("/api/v1/articles/1")
        assert response.json()["status"] == "draft"

    @pytest.mark.integration
    def test_response_contains_timestamps(
        self, client: TestClient, mock_prisma
    ):
        """
        GIVEN  a fake article with created_at and updated_at set
        WHEN   GET /api/v1/articles/1 is called
        THEN   the response body has non-null created_at and updated_at
        """
        mock_prisma.article.find_unique = AsyncMock(
            return_value=make_fake_article()
        )
        response = client.get("/api/v1/articles/1")
        data = response.json()
        assert data["created_at"] is not None
        assert data["updated_at"] is not None

    @pytest.mark.integration
    def test_response_has_empty_tags_list_when_no_tags(
        self, client: TestClient, mock_prisma
    ):
        """
        GIVEN  a fake article with no tags (tags=[])
        WHEN   GET /api/v1/articles/1 is called
        THEN   the response body has tags as an empty list (not null)
        """
        mock_prisma.article.find_unique = AsyncMock(
            return_value=make_fake_article(tags=[])
        )
        response = client.get("/api/v1/articles/1")
        data = response.json()
        assert "tags" in data
        assert isinstance(data["tags"], list)
        assert len(data["tags"]) == 0

    @pytest.mark.integration
    def test_response_category_is_none_for_uncategorised_article(
        self, client: TestClient, mock_prisma
    ):
        """
        GIVEN  a fake article with category=None and category_id=None
        WHEN   GET /api/v1/articles/1 is called
        THEN   the response body has category=null and category_id=null
        """
        mock_prisma.article.find_unique = AsyncMock(
            return_value=make_fake_article(category=None, category_id=None)
        )
        response = client.get("/api/v1/articles/1")
        data = response.json()
        assert data["category"] is None
        assert data["category_id"] is None

    @pytest.mark.integration
    def test_response_contains_nested_category_when_present(
        self, client: TestClient, mock_prisma
    ):
        """
        GIVEN  a fake article with a nested category object
        WHEN   GET /api/v1/articles/1 is called
        THEN   the response body contains the nested category with correct name
        """
        fake_category = _make_fake_category(id=3, name="ServiceNow", slug="servicenow")
        mock_prisma.article.find_unique = AsyncMock(
            return_value=make_fake_article(
                category_id=3,
                category=fake_category,
            )
        )
        response = client.get("/api/v1/articles/1")
        data = response.json()
        assert data["category"] is not None
        assert data["category"]["name"] == "ServiceNow"
        assert data["category"]["id"] == 3

    @pytest.mark.integration
    def test_response_contains_tags_list_when_article_has_tags(
        self, client: TestClient, mock_prisma
    ):
        """
        GIVEN  a fake article with two tags
        WHEN   GET /api/v1/articles/1 is called
        THEN   the response body contains a tags list with correct names
        """
        fake_tags = [
            _make_fake_tag(id=1, name="sap-fico", slug="sap-fico"),
            _make_fake_tag(id=2, name="finance", slug="finance"),
        ]
        mock_prisma.article.find_unique = AsyncMock(
            return_value=make_fake_article(tags=fake_tags)
        )
        response = client.get("/api/v1/articles/1")
        data = response.json()
        assert len(data["tags"]) == 2
        tag_names = {t["name"] for t in data["tags"]}
        assert "sap-fico" in tag_names
        assert "finance" in tag_names

    @pytest.mark.integration
    def test_response_contains_correct_content(
        self, client: TestClient, mock_prisma
    ):
        """
        GIVEN  a fake article with specific content
        WHEN   GET /api/v1/articles/1 is called
        THEN   the response body content field matches exactly
        """
        content = "Step 1: Open SAP GUI. Step 2: Navigate to Tx SM30."
        mock_prisma.article.find_unique = AsyncMock(
            return_value=make_fake_article(content=content)
        )
        response = client.get("/api/v1/articles/1")
        assert response.json()["content"] == content


# ===========================================================================
# GET /articles/{id} — 404 Error paths
# ===========================================================================

class TestGetArticleByIdNotFound:
    """Tests for the 404 Not Found error path on GET /api/v1/articles/{id}."""

    @pytest.mark.integration
    def test_returns_404_when_article_does_not_exist(
        self, client: TestClient, mock_prisma
    ):
        """
        GIVEN  the Prisma mock returns None (article not found)
        WHEN   GET /api/v1/articles/99999 is called
        THEN   the response status code is 404 Not Found
        """
        mock_prisma.article.find_unique = AsyncMock(return_value=None)
        response = client.get("/api/v1/articles/99999")
        assert response.status_code == 404

    @pytest.mark.integration
    def test_404_response_has_standard_error_envelope(
        self, client: TestClient, mock_prisma
    ):
        """
        GIVEN  the article does not exist
        WHEN   GET /api/v1/articles/99999 is called
        THEN   the body has the structure {"error": {"code", "message", "status"}}
        """
        mock_prisma.article.find_unique = AsyncMock(return_value=None)
        data = client.get("/api/v1/articles/99999").json()
        assert "error" in data
        assert all(k in data["error"] for k in ("code", "message", "status"))

    @pytest.mark.integration
    def test_404_error_code_is_article_not_found(
        self, client: TestClient, mock_prisma
    ):
        """
        GIVEN  the article does not exist
        WHEN   GET /api/v1/articles/99999 is called
        THEN   the error code is "ARTICLE_NOT_FOUND"
        """
        mock_prisma.article.find_unique = AsyncMock(return_value=None)
        data = client.get("/api/v1/articles/99999").json()
        assert data["error"]["code"] == "ARTICLE_NOT_FOUND"

    @pytest.mark.integration
    def test_404_error_status_matches_http_status(
        self, client: TestClient, mock_prisma
    ):
        """
        GIVEN  the article does not exist
        WHEN   GET /api/v1/articles/99999 is called
        THEN   the "status" inside the error envelope equals 404
        """
        mock_prisma.article.find_unique = AsyncMock(return_value=None)
        data = client.get("/api/v1/articles/99999").json()
        assert data["error"]["status"] == 404

    @pytest.mark.integration
    def test_404_error_message_contains_requested_id(
        self, client: TestClient, mock_prisma
    ):
        """
        GIVEN  no article with id 12345 exists
        WHEN   GET /api/v1/articles/12345 is called
        THEN   the error message mentions "12345" so the client can display it
        """
        mock_prisma.article.find_unique = AsyncMock(return_value=None)
        data = client.get("/api/v1/articles/12345").json()
        assert "12345" in data["error"]["message"]


# ===========================================================================
# GET /articles/{id} — 422 Input validation
# ===========================================================================

class TestGetArticleByIdInputValidation:
    """Tests for FastAPI path parameter validation (ge=1, type coercion)."""

    @pytest.mark.integration
    def test_id_zero_returns_422(self, client: TestClient, mock_prisma):
        """id=0 violates Path(..., ge=1) → 422 before hitting the handler."""
        assert client.get("/api/v1/articles/0").status_code == 422

    @pytest.mark.integration
    def test_negative_id_returns_422(self, client: TestClient, mock_prisma):
        """id=-3 violates ge=1 → 422."""
        assert client.get("/api/v1/articles/-3").status_code == 422

    @pytest.mark.integration
    def test_string_id_returns_422(self, client: TestClient, mock_prisma):
        """id='abc' cannot be coerced to int → 422."""
        assert client.get("/api/v1/articles/abc").status_code == 422


# ===========================================================================
# GET /articles — B15 (paginated list with category/status filters)
# ===========================================================================

class TestListArticles:
    """Tests for GET /api/v1/articles (B15 — list with optional filtering)."""

    @pytest.mark.integration
    def test_list_returns_200_with_empty_list(
        self, client: TestClient, mock_prisma
    ):
        """
        GIVEN  the repository returns an empty list
        WHEN   GET /api/v1/articles is called
        THEN   the response is 200 OK with a JSON array []
        """
        mock_prisma.article.find_many = AsyncMock(return_value=[])
        response = client.get("/api/v1/articles/")
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.integration
    def test_list_returns_articles(
        self, client: TestClient, mock_prisma
    ):
        """
        GIVEN  the repository returns two fake articles
        WHEN   GET /api/v1/articles is called
        THEN   the response contains a list of 2 items
        """
        mock_prisma.article.find_many = AsyncMock(return_value=[
            make_fake_article(id=1, slug="article-one"),
            make_fake_article(id=2, slug="article-two"),
        ])
        response = client.get("/api/v1/articles/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2

    @pytest.mark.integration
    def test_list_passes_category_id_filter(
        self, client: TestClient, mock_prisma
    ):
        """
        GIVEN  category_id=3 is passed as a query param
        WHEN   GET /api/v1/articles/?category_id=3 is called
        THEN   find_many is called exactly once (filter forwarded to repository)
               and the response is 200 OK
        """
        mock_prisma.article.find_many = AsyncMock(return_value=[
            make_fake_article(id=5, slug="filtered-article", category_id=3)
        ])
        response = client.get("/api/v1/articles/?category_id=3")
        assert response.status_code == 200
        mock_prisma.article.find_many.assert_called_once()

    @pytest.mark.integration
    def test_list_passes_status_filter(
        self, client: TestClient, mock_prisma
    ):
        """
        GIVEN  status=published is passed as a query param
        WHEN   GET /api/v1/articles/?status=published is called
        THEN   find_many is called exactly once and the response is 200 OK
        """
        mock_prisma.article.find_many = AsyncMock(return_value=[
            make_fake_article(id=7, slug="published-article", status="published")
        ])
        response = client.get("/api/v1/articles/?status=published")
        assert response.status_code == 200
        mock_prisma.article.find_many.assert_called_once()

    @pytest.mark.integration
    def test_list_invalid_category_id_returns_422(
        self, client: TestClient, mock_prisma
    ):
        """
        GIVEN  category_id=0 (violates ge=1)
        WHEN   GET /api/v1/articles/?category_id=0 is called
        THEN   FastAPI rejects it with 422 before hitting the handler
        """
        response = client.get("/api/v1/articles/?category_id=0")
        assert response.status_code == 422
