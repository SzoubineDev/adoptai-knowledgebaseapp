"""
B2 - FastAPI Application Entry Point (Minimal Bootstrap)
Project : AdoptAI App Knowledge Base
Author  : Oussama
Stage   : 1 (Foundation)

This is the minimal main.py for Stage 1.
It verifies that:
  - Settings load correctly from .env  (B2)
  - Prisma connects and disconnects cleanly on startup/shutdown  (B2)
  - CORS middleware is configured  (B2)
  - A basic /health endpoint is available for infrastructure probes.

Later stages will enrich this file with:
  - Centralized exception handlers (B20)
  - Versioned API router /api/v1 (B10, B12, B13, B15)
  - Full OpenAPI metadata (B26)

Run locally:
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Interactive API docs:
    http://localhost:8000/docs         (Swagger UI)
    http://localhost:8000/redoc        (ReDoc)
    http://localhost:8000/openapi.json (Raw schema)
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import prisma

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# B2 — Lifespan: Prisma connect / disconnect
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Manages the Prisma client lifecycle.

    - STARTUP : opens the connection pool to Supabase/PostgreSQL.
    - SHUTDOWN: gracefully closes all active connections.

    FastAPI's `lifespan` parameter replaces the deprecated
    `@app.on_event("startup")` / `@app.on_event("shutdown")` pattern.
    """
    logger.info("Connecting to database via Prisma…")
    await prisma.connect()
    logger.info("Prisma connected ✓")

    yield  # ← application is running here

    logger.info("Disconnecting Prisma…")
    await prisma.disconnect()
    logger.info("Prisma disconnected ✓")


# ---------------------------------------------------------------------------
# B2 — Application factory
# ---------------------------------------------------------------------------
def create_application() -> FastAPI:
    """
    Builds and configures the FastAPI application instance.

    Using a factory function (rather than module-level instantiation)
    makes the app testable: tests can call `create_application()` with
    dependency overrides without importing the global `app` directly.
    """
    application = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.APP_VERSION,
        description=settings.APP_DESCRIPTION,
        # Lifespan manages Prisma connect/disconnect (B2)
        lifespan=lifespan,
        # Doc URLs kept explicit for clarity
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # ------------------------------------------------------------------
    # CORS Middleware — origins loaded from ALLOWED_ORIGINS env var (B2)
    # ------------------------------------------------------------------
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return application


# ---------------------------------------------------------------------------
# Module-level app instance (used by uvicorn, pytest, gunicorn)
# ---------------------------------------------------------------------------
app: FastAPI = create_application()


# ---------------------------------------------------------------------------
# Health-check endpoint
# ---------------------------------------------------------------------------
@app.get(
    "/health",
    tags=["Health"],
    summary="Liveness probe",
    description=(
        "Returns `200 OK` with basic application metadata. "
        "Used by load balancers and uptime monitors to verify the process is alive. "
        "Does **not** check the database connection (use /health/db for that)."
    ),
    response_description="Application is running.",
)
def health_check() -> dict:
    """
    **Liveness probe** — confirms the API process is running.

    This endpoint intentionally avoids any database call so it remains fast
    and reliable even when the database is temporarily unreachable.
    """
    return {
        "status": "ok",
        "app": settings.PROJECT_NAME,
        "version": settings.APP_VERSION,
        "debug": settings.DEBUG,
        "api_prefix": settings.API_V1_STR,
    }


logger.info(
    "Application '%s' v%s initialized. Debug=%s",
    settings.PROJECT_NAME,
    settings.APP_VERSION,
    settings.DEBUG,
)
