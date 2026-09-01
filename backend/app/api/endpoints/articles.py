"""
B10 / B12 / B13 - Article Endpoints (GET, PUT, DELETE)
Project : AdoptAI App Knowledge Base
Author  : Oussama
Stages  : 3 & 4 (Core APIs & Advanced Endpoints)

This module defines the articles API router and implements:
  - GET    /articles/{id}  — B10  (Stage 3)
  - PUT    /articles/{id}  — B12  (Stage 4, wired now, implemented in next stage)
  - DELETE /articles/{id}  — B13  (Stage 4, wired now, implemented in next stage)

Architecture notes
------------------
* Router prefix `/articles` is applied in `app/api/router.py`.
* `get_prisma()` injects the connected Prisma client (async, B2).
* `article_repository` / `tag_repository` are Stage-2 Prisma singletons
  (repositories/__init__.py).
* All 404 paths raise `ArticleNotFoundException` (B19), caught and serialised
  by the centralised handler registered in `main.py` (B20).
* Response schema is `ArticleResponse` (B3) — no more stubs.
"""

import logging

from fastapi import APIRouter, Body, Depends, Path, Response, status
from prisma import Prisma

from app.core.database import get_prisma
from app.core.exceptions import ArticleNotFoundException, ArticleSlugConflictException
from app.repositories import article_repository, tag_repository
from app.schemas.article import ArticleResponse, ArticleUpdate

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------
router = APIRouter(tags=["Articles"])


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
    **GET /articles/{article_id}**

    Retrieves a knowledge-base article by its numeric primary key.

    - **article_id**: Must be a positive integer (`>= 1`). Non-integer or
      zero/negative values are rejected by FastAPI's path validation (422)
      before this handler is called.

    - On success, returns a full `ArticleResponse` with nested `category`
      and `tags` (loaded in the same Prisma query — no N+1).

    - Raises `ArticleNotFoundException` (B19 → 404) if no article with the
      given id exists. The exception is caught by the centralised handler
      registered in `main.py` (B20) and serialised into the standard error
      JSON envelope.
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
# PUT /articles/{id}  — B12 (implemented in Stage 4)
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
        "Returns the full updated article on success. "
        "Returns **404** if the article does not exist, "
        "**409** if the new slug is already taken by another article."
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

    **Validation flow**:
    1. Confirm the article exists → 404 if not.
    2. If a new `slug` is supplied, verify it is not used by another
       article → 409 if conflict.
    3. Delegate the update to `article_repository.update()` (Prisma).
    4. Return the updated article with relations.
    """
    logger.info("PUT /articles/%s — update requested", article_id)

    # Step 1: Confirm existence.
    existing = await article_repository.get(db, article_id)
    if existing is None:
        logger.warning("PUT /articles/%s — article not found (404)", article_id)
        raise ArticleNotFoundException(article_id)

    # Step 2: Slug uniqueness guard.
    if body.slug is not None and body.slug != existing.slug:
        if await article_repository.slug_exists(db, body.slug, exclude_id=article_id):
            logger.warning(
                "PUT /articles/%s — slug conflict: %r", article_id, body.slug
            )
            raise ArticleSlugConflictException(body.slug)

    # Step 3: Delegate update to Prisma repository.
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
# DELETE /articles/{id}  — B13 (implemented in Stage 4)
# ---------------------------------------------------------------------------

@router.delete(
    "/{article_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an article by ID",
    description=(
        "Permanently deletes a knowledge-base article and all its tag associations. "
        "Returns **204 No Content** on success (no response body). "
        "Returns **404** if the article does not exist."
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

    - The `article_tags` join-table rows are removed automatically by the
      PostgreSQL `ON DELETE CASCADE` constraint — no manual cleanup needed.
    - Returns HTTP **204 No Content** with an empty body on success.
    - Raises `ArticleNotFoundException` (B19 → 404) if no article with the
      given id exists.
    """
    logger.info("DELETE /articles/%s — deletion requested", article_id)

    # Step 1: Confirm existence before attempting deletion.
    existing = await article_repository.get(db, article_id)
    if existing is None:
        logger.warning("DELETE /articles/%s — article not found (404)", article_id)
        raise ArticleNotFoundException(article_id)

    # Step 2: Delete via Prisma repository.
    await article_repository.delete(db, article_id=article_id)

    logger.info("DELETE /articles/%s — deleted successfully", article_id)

    # Return an explicit empty 204 Response so FastAPI does not attempt
    # to serialise None (which would cause a runtime error).
    return Response(status_code=status.HTTP_204_NO_CONTENT)
