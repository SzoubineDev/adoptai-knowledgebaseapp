"""
B25 - Tag Repository (Prisma)
Project : AdoptAI App Knowledge Base
Author  : Oussama
Stage   : 2 (Data Access)

Implements all data-access operations for the `Tag` entity using the
Prisma Client Python async client.

Key responsibilities
--------------------
* Look up tags by id, name, or slug.
* Fetch multiple tags in a single batched query (used when resolving
  tag_ids supplied in article create / update payloads).
* Create new tags.
* Get-or-create helpers for upsert-style tag assignment.
* Delete a tag (cascade handled by the DB via article_tags FK).
* Existence / uniqueness guards used by route handlers before write ops.

Design principles
-----------------
* The Prisma client is always passed in as `db: Prisma` — never stored
  as instance state — so the repository is fully stateless and can be
  safely shared as a module-level singleton.
* All methods are `async` to match the Prisma async client's interface.
* No transaction commits here: the caller (route handler) owns the
  transaction boundary.
* `find_unique` raises `prisma.errors.RecordNotFoundError` on miss when
  `raise_not_found` would be appropriate; we capture and return None
  instead, letting the caller decide whether to raise a domain exception.
"""

from typing import List, Optional

from prisma import Prisma
from prisma.models import Tag as PrismaTag


class TagRepository:
    """
    Stateless async repository for Tag CRUD operations using Prisma.

    All public methods are coroutines — call them with `await`.

    Usage in a FastAPI route:
        from app.repositories import tag_repository
        from app.core.database import get_prisma
        from fastapi import Depends
        from prisma import Prisma

        @router.get("/tags/{tag_id}")
        async def get_tag(
            tag_id: int,
            db: Prisma = Depends(get_prisma),
        ):
            tag = await tag_repository.get(db, tag_id)
            ...
    """

    # ------------------------------------------------------------------
    # READ operations
    # ------------------------------------------------------------------

    async def get(self, db: Prisma, tag_id: int) -> Optional[PrismaTag]:
        """
        Fetch a single Tag by primary key.

        Returns None if no tag with the given id exists.
        """
        return await db.tag.find_unique(where={"id": tag_id})

    async def get_by_name(self, db: Prisma, name: str) -> Optional[PrismaTag]:
        """
        Fetch a Tag by its human-readable name (case-sensitive).

        Used to check for duplicates before creating a new tag, and to
        resolve tag names supplied in article payloads.

        Returns None if the name does not exist.
        """
        return await db.tag.find_first(where={"name": name})

    async def get_by_slug(self, db: Prisma, slug: str) -> Optional[PrismaTag]:
        """
        Fetch a Tag by its URL-safe slug.

        Returns None if the slug does not exist.
        """
        return await db.tag.find_first(where={"slug": slug})

    async def get_many(
        self,
        db: Prisma,
        *,
        skip: int = 0,
        limit: int = 50,
    ) -> List[PrismaTag]:
        """
        Return a paginated list of all tags ordered alphabetically by name.

        Used for admin tag management and autocomplete suggestions.

        Parameters
        ----------
        skip  : Pagination offset (maps to Prisma's `skip`).
        limit : Page size (maps to Prisma's `take`), capped at 200.
        """
        limit = min(limit, 200)
        return await db.tag.find_many(
            skip=skip,
            take=limit,
            order={"name": "asc"},
        )

    async def get_by_ids(self, db: Prisma, tag_ids: List[int]) -> List[PrismaTag]:
        """
        Fetch multiple Tags by a list of primary keys in a single query.

        Used by the Article repository's create/update path when the API
        caller supplies tag IDs directly.

        Returns only the tags that actually exist; silently ignores
        non-existent IDs. The route handler validates completeness if
        strict validation is required.
        """
        if not tag_ids:
            return []
        return await db.tag.find_many(where={"id": {"in": tag_ids}})

    async def count(self, db: Prisma) -> int:
        """Return the total number of tags in the database."""
        return await db.tag.count()

    async def name_exists(
        self,
        db: Prisma,
        name: str,
        exclude_id: Optional[int] = None,
    ) -> bool:
        """
        Check whether a tag name is already taken.

        `exclude_id` allows the current tag's own name to be excluded
        during an update so unchanged names don't trigger false conflicts.

        Returns True if the name is taken, False otherwise.
        """
        where: dict = {"name": name}
        if exclude_id is not None:
            where["NOT"] = {"id": exclude_id}
        result = await db.tag.find_first(where=where)
        return result is not None

    async def slug_exists(
        self,
        db: Prisma,
        slug: str,
        exclude_id: Optional[int] = None,
    ) -> bool:
        """
        Check whether a tag slug is already taken.

        Same `exclude_id` pattern as `name_exists` for update idempotency.

        Returns True if the slug is taken, False otherwise.
        """
        where: dict = {"slug": slug}
        if exclude_id is not None:
            where["NOT"] = {"id": exclude_id}
        result = await db.tag.find_first(where=where)
        return result is not None

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------

    async def create(self, db: Prisma, *, name: str, slug: str) -> PrismaTag:
        """
        Persist a new Tag to the database.

        Parameters
        ----------
        name : Human-readable tag label. Must be unique (the caller
               should verify with `name_exists` first, or rely on the
               DB unique constraint to raise an IntegrityError).
        slug : URL-safe unique identifier.

        Returns the created Tag instance with all DB-assigned fields
        (`id`, `created_at`) populated.
        """
        return await db.tag.create(data={"name": name, "slug": slug})

    # ------------------------------------------------------------------
    # GET-OR-CREATE  (most critical helper for article tag management)
    # ------------------------------------------------------------------

    async def get_or_create(
        self,
        db: Prisma,
        *,
        name: str,
        slug: str,
    ) -> tuple[PrismaTag, bool]:
        """
        Return an existing Tag that matches `name`, or create a new one.

        Returns
        -------
        (tag, created)
            tag     : The Tag Prisma model (existing or newly created).
            created : True if the tag was just created, False if it existed.

        This is the safest single-tag upsert primitive — the route handler
        can surface the `created` flag in the response if desired.
        """
        existing = await self.get_by_name(db, name)
        if existing is not None:
            return existing, False

        new_tag = await self.create(db, name=name, slug=slug)
        return new_tag, True

    async def get_or_create_many(
        self,
        db: Prisma,
        tag_inputs: List[dict],
    ) -> List[PrismaTag]:
        """
        Resolve a list of tag payloads to Prisma Tag instances, creating
        any tags that do not yet exist — in as few queries as possible.

        Parameters
        ----------
        tag_inputs : List of dicts, each with keys:
                     - "name" (str, required)
                     - "slug" (str, required)

        Query strategy
        --------------
        1. One batch `find_many` to fetch all tags whose names are in input.
        2. For each name NOT found, one `create` call.
        This yields at most 1 + N_new queries regardless of list size.

        Returns a list of Tag instances in the same order as `tag_inputs`.
        """
        if not tag_inputs:
            return []

        # Step 1: Batch-fetch all existing tags whose names are in the list.
        names = [t["name"] for t in tag_inputs]
        existing_tags_list = await db.tag.find_many(
            where={"name": {"in": names}}
        )
        existing_map: dict[str, PrismaTag] = {
            tag.name: tag for tag in existing_tags_list
        }

        # Step 2: Create any tags that were not found; preserve input order.
        result: List[PrismaTag] = []
        for payload in tag_inputs:
            name = payload["name"]
            slug = payload["slug"]
            if name in existing_map:
                result.append(existing_map[name])
            else:
                new_tag = await self.create(db, name=name, slug=slug)
                existing_map[name] = new_tag  # Prevent duplicate inserts
                result.append(new_tag)        # within the same call.

        return result

    # ------------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------------

    async def update(
        self,
        db: Prisma,
        *,
        tag_id: int,
        name: Optional[str] = None,
        slug: Optional[str] = None,
    ) -> Optional[PrismaTag]:
        """
        Apply a partial update to an existing Tag.

        Only fields that are explicitly passed (not None) are modified.

        Returns the updated Tag, or None if no tag with `tag_id` exists.
        """
        data: dict = {}
        if name is not None:
            data["name"] = name
        if slug is not None:
            data["slug"] = slug

        if not data:
            # Nothing to update — return current state.
            return await self.get(db, tag_id)

        try:
            return await db.tag.update(where={"id": tag_id}, data=data)
        except Exception:
            # Prisma raises if the record does not exist; return None
            # to let the caller raise the appropriate domain exception.
            return None

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------

    async def delete(self, db: Prisma, *, tag_id: int) -> bool:
        """
        Delete a Tag by primary key.

        The `ondelete="CASCADE"` on the `article_tags` join table ensures
        all association rows referencing this tag are removed automatically
        by the database — no manual cleanup needed.

        Returns True if the tag was deleted, False if it did not exist.
        """
        try:
            await db.tag.delete(where={"id": tag_id})
            return True
        except Exception:
            return False
