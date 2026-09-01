"""
B2 - Prisma Client Python — Database Connection Manager
Project : AdoptAI App Knowledge Base
Author  : Oussama
Stage   : 1 (Foundation)

Replaces the SQLAlchemy engine with the official Prisma Client Python
async client, which connects directly to Supabase (PostgreSQL) using
the PRISMA_DATABASE_URL environment variable.

Architecture:
  - `prisma` singleton is instantiated at module level (lazy connection).
  - FastAPI's `lifespan` context manager calls connect() / disconnect()
    at app startup / shutdown — ensuring clean connection lifecycle.
  - `get_prisma()` is a FastAPI dependency that injects the connected
    client into route handlers.

Requirements:
    prisma-client-py  (pip install prisma)
    PRISMA_DATABASE_URL set in .env
"""

from collections.abc import AsyncGenerator

from prisma import Prisma

from app.core.config import settings

# ---------------------------------------------------------------------------
# Prisma Client singleton
# ---------------------------------------------------------------------------
# Instantiated at import time; actual TCP connection is established later
# by calling `await prisma.connect()` inside the FastAPI lifespan handler.
# ---------------------------------------------------------------------------
prisma: Prisma = Prisma(
    datasource={"url": settings.PRISMA_DATABASE_URL}
    if settings.PRISMA_DATABASE_URL
    else None,
)


# ---------------------------------------------------------------------------
# FastAPI Dependency – Prisma Client
# ---------------------------------------------------------------------------
async def get_prisma() -> AsyncGenerator[Prisma, None]:
    """
    FastAPI dependency that yields the connected Prisma client.

    The client is connected during the application lifespan (see main.py),
    so this dependency simply yields the already-connected singleton without
    re-opening a connection on every request.

    Usage in a route:
        from prisma import Prisma
        from fastapi import Depends
        from app.core.database import get_prisma

        @router.get("/example")
        async def example(db: Prisma = Depends(get_prisma)):
            return await db.article.find_many()
    """
    yield prisma


# Backward-compatibility alias for legacy imports
get_db = get_prisma


# ---------------------------------------------------------------------------
# Health-check helper
# ---------------------------------------------------------------------------
async def check_database_connection() -> bool:
    """
    Performs a lightweight query to verify the Prisma/PostgreSQL connection.
    Returns True if healthy, False otherwise.
    Used by the /health endpoint (optional readiness probe).
    """
    try:
        # `query_raw` with a trivial SELECT is the lightest possible probe.
        await prisma.query_raw("SELECT 1")
        return True
    except Exception:
        return False
