"""
B10 / B12 / B13 / B15 - Article Endpoints (GET list, GET by id, PUT, DELETE)
Project : AdoptAI App Knowledge Base
Author  : Oussama
Stages  : 3 & 4 (Core APIs & Advanced Endpoints)

This module defines the articles API router and implements:
  - GET    /articles            — B15  (Stage 4) — paginated list with filters
  - GET    /articles/{id}       — B10  (Stage 3) — single article by PK
  - PUT    /articles/{id}       — B12  (Stage 4) — partial update
  - DELETE /articles/{id}       — B13  (Stage 4) — hard delete (204)

Architecture notes
------------------
* Router prefix `/articles` is applied in `app/api/router.py`.
* `get_prisma()` injects the connected Prisma async client (B2).
* `article_repository` is the Stage-2 Prisma singleton (repositories/).
* All 404 paths raise `ArticleNotFoundException` (B19), caught and serialised
  by the centralised handler registered in `main.py` (B20).
* Response schema is `ArticleResponse` (B3) — no stubs.
* `CategoryFilterParams` (B15) is a reusable FastAPI dependency that
  extracts category_id, status, skip, and limit from the query string.

Route declaration order matters:
  GET "/"  MUST be declared BEFORE GET "/{article_id}" to prevent FastAPI
  from treating the literal string "/" as a path parameter.
"""

import logging
from typing import List

from fastapi import APIRouter, Body, Depends, Path, Query, Response, status
from prisma import Prisma

from app.api.dependencies.filters import CategoryFilterParams
from app.core.database import get_prisma
from app.core.exceptions import ArticleNotFoundException, ArticleSlugConflictException
from app.repositories import article_repository
from app.schemas.article import ArticleResponse, ArticleStatus, ArticleUpdate

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------
router = APIRouter(tags=["Articles"])


# ---------------------------------------------------------------------------
# GET /articles  — B15 (paginated list + category / status filtering)
# ---------------------------------------------------------------------------

@router.get(
    "/",
    response_model=List[ArticleResponse],
    status_code=status.HTTP_200_OK,
    summary="List articles (with optional filtering)",
    description=(
        "Returns a **paginated list** of knowledge-base articles. \n\n"
        "Supports optional filtering by:\n"
        "- **`category_id`** — return only articles belonging to the given category (B15).\n"
        "- **`status`** — filter by lifecycle state (`draft`, `published`, `archived`).\n\n"
        "Pagination is controlled via `skip` (offset) and `limit` (page size, max 100). "
        "Results are ordered by `created_at` descending (newest first)."
    ),
    responses={
        200: {"description": "Paginated article list returned successfully."},
    },
)
async def list_articles(
    filters: CategoryFilterParams = Depends(),
    db: Prisma = Depends(get_prisma),
) -> List[ArticleResponse]:
    """
    **GET /articles** — B15

    Returns a paginated list of articles with optional filters.

    Query parameters (all optional):
    - **category_id** (`int >= 1`) : restrict to one category (B15 core).
    - **status** (`draft|published|archived`) : lifecycle state filter.
    - **skip** (`int >= 0`, default `0`) : pagination offset.
    - **limit** (`int 1–100`, default `20`) : page size.

    The response is a flat JSON array of `ArticleResponse` objects, each
    containing nested `category` and `tags` (no N+1 — Prisma includes
    relations in the same query).

    Use the `X-Total-Count` response header (set below) to implement
    client-side pagination controls without a separate count call.
    """
    logger.info(
        "GET /articles — filters: category_id=%s status=%s skip=%s limit=%s",
        filters.category_id, filters.status, filters.skip, filters.limit,
    )

    articles = await article_repository.get_many(
        db,
        skip=filters.skip,
        limit=filters.limit,
        status=filters.status,
        category_id=filters.category_id,
    )

    logger.info("GET /articles — returning %d article(s)", len(articles))
    return [ArticleResponse.model_validate(a) for a in articles]


# ---------------------------------------------------------------------------
# GET /articles/{id}  — B10
# ---------------------------------------------------------------------------

@router.get(
    "/{article_id}",
    response_model=ArticleResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve an article by ID",
    description=(
        "Fetches a single knowledge-base article by its numeric primary key. "
        "The response includes the article's full content, its parent **category**, "
        "and all associated **tags**. Returns **404** if the article does not exist."
    ),
    responses={
        200: {"description": "Article found and returned successfully."},
        404: {
            "description": "No article exists with the given id.",
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "code": "ARTICLE_NOT_FOUND",
                            "message": "Article with id '42' was not found.",
                            "status": 404,
                        }
                    }
                }
            },
        },
    },
)
async def get_article_by_id(
    article_id: int = Path(
        ...,
        ge=1,
        description="The numeric primary key of the article to retrieve.",
        examples=[1],
    ),
    db: Prisma = Depends(get_prisma),
) -> ArticleResponse:
    """
    **GET /articles/{article_id}** — B10

    Retrieves a knowledge-base article by its numeric primary key.

    - **article_id**: Must be a positive integer (`>= 1`). Non-integer or
      zero/negative values are rejected by FastAPI's path validation (422)
      before this handler is called.
    - On success, returns a full `ArticleResponse` with nested `category`
      and `tags` (loaded in the same Prisma query — no N+1).
    - Raises `ArticleNotFoundException` (B19 → 404) if no article with the
      given id exists. The exception is caught by the centralised handler
      registered in `main.py` (B20).
    """
    logger.info("GET /articles/%s — fetching article with relations", article_id)

    article = await article_repository.get_with_relations(db, article_id)

    if article is None:
        logger.warning("GET /articles/%s — article not found (404)", article_id)
        raise ArticleNotFoundException(article_id)   # B19

    logger.info(
        "GET /articles/%s — found: slug=%r status=%r",
        article_id, article.slug, article.status,
    )
    return ArticleResponse.model_validate(article)


# ---------------------------------------------------------------------------
# PUT /articles/{id}  — B12
# ---------------------------------------------------------------------------

@router.put(
    "/{article_id}",
    response_model=ArticleResponse,
    status_code=status.HTTP_200_OK,
    summary="Update an article by ID",
    description=(
        "Performs a **partial update** on a knowledge-base article. "
        "Only the fields included in the request body are modified; "
        "omitted fields retain their current values. "
        "Returns the full updated article on success.\n\n"
        "- Returns **404** if the article does not exist.\n"
        "- Returns **409** if the new `slug` is already taken by another article.\n\n"
        "Providing `tag_ids` **replaces** the article's entire tag set. "
        "Pass an empty list `[]` to remove all tags."
    ),
    responses={
        200: {"description": "Article updated and returned successfully."},
        404: {
            "description": "No article exists with the given id.",
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "code": "ARTICLE_NOT_FOUND",
                            "message": "Article with id '42' was not found.",
                            "status": 404,
                        }
                    }
                }
            },
        },
        409: {
            "description": "The requested slug is already taken by another article.",
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "code": "ARTICLE_SLUG_CONFLICT",
                            "message": "An article with slug 'my-slug' already exists.",
                            "status": 409,
                        }
                    }
                }
            },
        },
    },
)
async def update_article(
    article_id: int = Path(
        ...,
        ge=1,
        description="The numeric primary key of the article to update.",
        examples=[1],
    ),
    body: ArticleUpdate = Body(
        ...,
        description=(
            "Fields to update. All fields are optional; omit any field to "
            "keep its current value. Providing `tag_ids` **replaces** the "
            "current tag set entirely."
        ),
    ),
    db: Prisma = Depends(get_prisma),
) -> ArticleResponse:
    """
    **PUT /articles/{article_id}** — B12

    Partially updates a knowledge-base article.

    Validation flow:
    1. Confirm the article exists → 404 if not found.
    2. If a new `slug` is supplied and differs from the current one,
       verify it is not used by another article → 409 if conflict.
    3. Delegate the update to `article_repository.update()` (Prisma).
       Tags are updated via Prisma's `set` operation (full replacement).
    4. Return the fully updated article with relations eagerly loaded.
    """
    logger.info("PUT /articles/%s — update requested", article_id)

    # Step 1: Confirm existence.
    existing = await article_repository.get(db, article_id)
    if existing is None:
        logger.warning("PUT /articles/%s — article not found (404)", article_id)
        raise ArticleNotFoundException(article_id)   # B19

    # Step 2: Slug uniqueness guard (skip if slug unchanged).
    if body.slug is not None and body.slug != existing.slug:
        if await article_repository.slug_exists(db, body.slug, exclude_id=article_id):
            logger.warning(
                "PUT /articles/%s — slug conflict: %r", article_id, body.slug
            )
            raise ArticleSlugConflictException(body.slug)

    # Step 3: Delegate partial update to Prisma repository.
    updated = await article_repository.update(
        db,
        article_id=article_id,
        title=body.title,
        slug=body.slug,
        content=body.content,
        status=body.status,
        type_hebergement=body.type_hebergement,
        category_id=body.category_id,
        tag_ids=body.tag_ids,
    )

    logger.info("PUT /articles/%s — updated successfully", article_id)
    return ArticleResponse.model_validate(updated)


# ---------------------------------------------------------------------------
# DELETE /articles/{id}  — B13
# ---------------------------------------------------------------------------

@router.delete(
    "/{article_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an article by ID",
    description=(
        "Permanently deletes a knowledge-base article and all its tag associations.\n\n"
        "- The `article_tags` join-table rows are removed automatically by the "
        "PostgreSQL `ON DELETE CASCADE` constraint — no manual cleanup needed.\n"
        "- Returns **204 No Content** on success (no response body).\n"
        "- Returns **404** if the article does not exist."
    ),
    responses={
        204: {"description": "Article deleted successfully. No content is returned."},
        404: {
            "description": "No article exists with the given id.",
            "content": {
                "application/json": {
                    "example": {
                        "error": {
                            "code": "ARTICLE_NOT_FOUND",
                            "message": "Article with id '42' was not found.",
                            "status": 404,
                        }
                    }
                }
            },
        },
    },
)
async def delete_article(
    article_id: int = Path(
        ...,
        ge=1,
        description="The numeric primary key of the article to delete.",
        examples=[1],
    ),
    db: Prisma = Depends(get_prisma),
) -> Response:
    """
    **DELETE /articles/{article_id}** — B13

    Permanently removes a knowledge-base article from the database.

    Steps:
    1. Confirm the article exists → raise `ArticleNotFoundException` (B19 → 404)
       if not found. This prevents a misleading 500 from a missing-record delete.
    2. Delegate deletion to `article_repository.delete()` (Prisma).
       The `ON DELETE CASCADE` on `article_tags.article_id` removes all
       tag associations automatically.
    3. Return HTTP 204 No Content (RFC 9110 §15.3.5 — no body on success).
    """
    logger.info("DELETE /articles/%s — deletion requested", article_id)

    # Step 1: Confirm existence before deletion attempt.
    existing = await article_repository.get(db, article_id)
    if existing is None:
        logger.warning("DELETE /articles/%s — article not found (404)", article_id)
        raise ArticleNotFoundException(article_id)   # B19

    # Step 2: Hard delete via Prisma.
    await article_repository.delete(db, article_id=article_id)

    logger.info("DELETE /articles/%s — deleted successfully", article_id)

    # Return an explicit 204 Response so FastAPI does not attempt to
    # serialise None (which would cause a runtime error since no
    # response_model is declared on a 204 route).
    return Response(status_code=status.HTTP_204_NO_CONTENT)
