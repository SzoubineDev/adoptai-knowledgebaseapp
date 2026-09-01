"""
B23 - Article Repository (Prisma)
Project : AdoptAI App Knowledge Base
Author  : Oussama
Stage   : 2 (Data Access)

Implements all data-access operations for the `Article` entity using the
Prisma Client Python async client.

Design principles
-----------------
* The Prisma client (`db: Prisma`) is ALWAYS passed in as a parameter —
  never stored as instance state — keeping the repository fully stateless
  and safely shareable as a module-level singleton.
* All methods are `async` to match Prisma's native async interface.
* Relations (category, tags) are loaded in the SAME query via Prisma's
  `include` argument — preventing N+1 queries at the serialisation layer.
* No transaction commits here: the caller (route handler) owns the
  transaction boundary.

Prisma query patterns used
--------------------------
  find_unique  → fetch by primary key
  find_first   → fetch by slug (unique but not PK)
  find_many    → paginated list with optional filters
  create       → insert a new article with nested tag connections
  update       → patch scalar fields + reconnect tags
  delete       → hard delete by PK (FK cascade removes article_tags rows)
  count        → total rows for pagination metadata

Relation include block (reused across all fetch methods)
---------------------------------------------------------
    _INCLUDE = {
        "category": True,
        "tags":     True,
    }
This tells Prisma to perform a JOIN (or subquery, depending on the DB)
and return the related objects in the same result object.
"""

from typing import Dict, List, Optional

from prisma import Prisma
from prisma.models import Article as PrismaArticle

from app.schemas.article import ArticleStatus, TypeHebergement

# ---------------------------------------------------------------------------
# Shared Prisma include block — loads category + tags in every SELECT.
# Defined at module level to avoid duplication and keep queries DRY.
# ---------------------------------------------------------------------------
_INCLUDE: Dict = {
    "category": True,
    "tags": True,
}


class ArticleRepository:
    """
    Stateless async repository for Article CRUD operations using Prisma.

    All public methods are coroutines — always call them with `await`.

    Usage in a FastAPI route:
        from app.repositories import article_repository
        from app.core.database import get_prisma
        from fastapi import Depends
        from prisma import Prisma

        @router.get("/articles/{article_id}")
        async def get_article(
            article_id: int,
            db: Prisma = Depends(get_prisma),
        ):
            article = await article_repository.get_with_relations(db, article_id)
            ...
    """

    # ------------------------------------------------------------------
    # READ operations
    # ------------------------------------------------------------------

    async def get(self, db: Prisma, article_id: int) -> Optional[PrismaArticle]:
        """
        Fetch a single Article by primary key WITHOUT loading relations.

        Use this for lightweight existence checks or status-only operations
        where you don't need category/tag data.

        Returns None if no article with the given id exists.
        """
        return await db.article.find_unique(where={"id": article_id})

    async def get_with_relations(
        self,
        db: Prisma,
        article_id: int,
    ) -> Optional[PrismaArticle]:
        """
        Fetch a single Article by primary key WITH Category and Tags loaded.

        Prisma fetches relations in the same query via `include`, so no
        N+1 issue arises when serialising the ArticleResponse schema.

        Use this as the primary fetch method for:
          - GET  /articles/{id}   (B10)
          - PUT  /articles/{id}   (B12) — to return the updated state

        Returns None if no article with the given id exists.
        """
        return await db.article.find_unique(
            where={"id": article_id},
            include=_INCLUDE,
        )

    async def get_by_slug(
        self,
        db: Prisma,
        slug: str,
    ) -> Optional[PrismaArticle]:
        """
        Fetch a single Article by its URL-safe slug WITH relations.

        Slugs are unique (DB-enforced), so at most one row is returned.
        Returns None if the slug does not exist.
        """
        return await db.article.find_first(
            where={"slug": slug},
            include=_INCLUDE,
        )

    async def get_many(
        self,
        db: Prisma,
        *,
        skip: int = 0,
        limit: int = 20,
        status: Optional[ArticleStatus] = None,
        category_id: Optional[int] = None,
    ) -> List[PrismaArticle]:
        """
        Return a paginated list of articles with optional filters.

        Parameters
        ----------
        skip        : Rows to skip (Prisma `skip`) — for page-based pagination.
        limit       : Max rows to return (Prisma `take`) — hard-capped at 100.
        status      : Filter by ArticleStatus value ("draft" | "published" | "archived").
        category_id : Filter by category FK — used by B15 (category filtering).

        WHERE clauses are built conditionally so unused filters add no overhead.
        Relations are included to avoid N+1 on list serialisation.
        """
        limit = min(limit, 100)  # Protect against unbounded result sets.

        where: Dict = {}
        if status is not None:
            where["status"] = status.value
        if category_id is not None:
            where["categoryId"] = category_id

        return await db.article.find_many(
            where=where,
            include=_INCLUDE,
            skip=skip,
            take=limit,
            order={"createdAt": "desc"},
        )

    async def count(
        self,
        db: Prisma,
        *,
        status: Optional[ArticleStatus] = None,
        category_id: Optional[int] = None,
    ) -> int:
        """
        Return the total number of articles matching the given filters.

        Used alongside `get_many` to compute pagination metadata
        (total_pages, total_items, etc.) without fetching full rows.
        """
        where: Dict = {}
        if status is not None:
            where["status"] = status.value
        if category_id is not None:
            where["categoryId"] = category_id

        return await db.article.count(where=where)

    async def slug_exists(
        self,
        db: Prisma,
        slug: str,
        exclude_id: Optional[int] = None,
    ) -> bool:
        """
        Check whether a given slug is already taken by another article.

        `exclude_id` allows the current article's own slug to be excluded
        during a PUT update so unchanged slugs don't falsely flag a conflict.

        Returns True if the slug is taken, False otherwise.
        """
        where: Dict = {"slug": slug}
        if exclude_id is not None:
            where["NOT"] = {"id": exclude_id}
        result = await db.article.find_first(where=where)
        return result is not None

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------

    async def create(
        self,
        db: Prisma,
        *,
        title: str,
        slug: str,
        content: str,
        status: ArticleStatus = ArticleStatus.DRAFT,
        type_hebergement: Optional[TypeHebergement] = None,
        category_id: Optional[int] = None,
        tag_ids: Optional[List[int]] = None,
    ) -> PrismaArticle:
        """
        Persist a new Article to the database.

        Parameters
        ----------
        title            : Article headline.
        slug             : URL-safe unique identifier.
        content          : Full article body (plain text or Markdown).
        status           : Initial lifecycle state (defaults to DRAFT).
        type_hebergement : Optional hosting context enum.
        category_id      : Optional FK to an existing Category.
        tag_ids          : Optional list of existing Tag IDs to associate.

        Tags are connected via Prisma's nested `connect` syntax so the
        article_tags join table is populated in the same transaction.

        Returns the created Article with relations included.
        """
        data: Dict = {
            "title": title,
            "slug": slug,
            "content": content,
            "status": status.value,
        }

        if type_hebergement is not None:
            data["typeHebergement"] = type_hebergement.value

        if category_id is not None:
            data["category"] = {"connect": {"id": category_id}}

        if tag_ids:
            data["tags"] = {
                "connect": [{"id": tid} for tid in tag_ids]
            }

        return await db.article.create(data=data, include=_INCLUDE)

    # ------------------------------------------------------------------
    # UPDATE  (B12)
    # ------------------------------------------------------------------

    async def update(
        self,
        db: Prisma,
        *,
        article_id: int,
        title: Optional[str] = None,
        slug: Optional[str] = None,
        content: Optional[str] = None,
        status: Optional[ArticleStatus] = None,
        type_hebergement: Optional[TypeHebergement] = None,
        category_id: Optional[int] = None,
        tag_ids: Optional[List[int]] = None,
    ) -> Optional[PrismaArticle]:
        """
        Apply a partial update to an existing Article.

        Only fields that are explicitly passed (not None) are modified,
        implementing PATCH semantics through a PUT endpoint — the route
        handler forwards only the supplied fields.

        Tag update strategy — FULL REPLACEMENT via Prisma's `set`:
            When `tag_ids` is provided (even as []), the current tag set is
            replaced entirely. Omitting `tag_ids` (None) leaves tags unchanged.
            This matches the contract documented in ArticleUpdate.

        Returns the updated Article with relations included, or None if
        no article with the given `article_id` exists.
        """
        data: Dict = {}

        if title is not None:
            data["title"] = title
        if slug is not None:
            data["slug"] = slug
        if content is not None:
            data["content"] = content
        if status is not None:
            data["status"] = status.value
        if type_hebergement is not None:
            data["typeHebergement"] = type_hebergement.value
        if category_id is not None:
            data["category"] = {"connect": {"id": category_id}}
        if tag_ids is not None:
            # `set` disconnects all previous tags and connects the new list.
            data["tags"] = {
                "set": [{"id": tid} for tid in tag_ids]
            }

        if not data:
            # Nothing to update — return current state with relations.
            return await self.get_with_relations(db, article_id)

        try:
            return await db.article.update(
                where={"id": article_id},
                data=data,
                include=_INCLUDE,
            )
        except Exception:
            # Prisma raises if the record does not exist.
            return None

    # ------------------------------------------------------------------
    # DELETE  (B13)
    # ------------------------------------------------------------------

    async def delete(self, db: Prisma, *, article_id: int) -> bool:
        """
        Hard-delete an Article by primary key.

        The `ondelete="CASCADE"` on `article_tags.article_id` ensures all
        join-table rows for this article are removed automatically by the
        database — no manual cleanup is needed.

        Returns True if the article was deleted, False if it did not exist.
        """
        try:
            await db.article.delete(where={"id": article_id})
            return True
        except Exception:
            return False
