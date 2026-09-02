"""
B2 / B20 / B10 / B26 / Auth Étape 4 - FastAPI Application Entry Point
Project : AdoptAI App Knowledge Base
Author  : Oussama
Stages  : 1 (Foundation), 3 (Core APIs & Errors), 5 (Docs & Tests), Feature Auth

This module is the top-level application factory. It:
  1. Loads settings from .env via Pydantic BaseSettings (B2).
  2. Manages the Prisma client lifecycle via lifespan (B2).
  3. Configures CORS middleware (B2).
  4. Registers all centralized exception handlers (B20).
  5. Mounts the versioned API router /api/v1 (B10).
  6. Exposes a /health liveness probe.
  7. Provides exhaustive OpenAPI metadata (B26):
       - Rich Markdown API description with tables
       - Contact & license blocks (rendered in ReDoc sidebar)
       - Named tag definitions with descriptions (groups endpoints in Swagger UI)
       - Custom openapi() hook to inject servers block and x-logo
       - Swagger UI parameters for a polished developer experience

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
from fastapi.openapi.utils import get_openapi

from app.api.router import api_router
from app.core.config import settings
from app.core.database import prisma
from app.core.error_handlers import register_exception_handlers

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
# B26 — OpenAPI tag definitions
# ---------------------------------------------------------------------------
# Each entry creates a named, described section in Swagger UI.
# Tags must match the `tags=[...]` values in the router decorators.
# ---------------------------------------------------------------------------
OPENAPI_TAGS: list[dict] = [
    {
        "name": "Articles",
        "description": (
            "Operations on **knowledge-base articles**.\n\n"
            "Articles are the core content unit of AdoptAI — they contain "
            "step-by-step guidance, FAQs, and how-to content for enterprise "
            "applications (SAP, ServiceNow, Apple MDM, etc.).\n\n"
            "Each article belongs to one **Category** (nullable) and may "
            "carry multiple **Tags** (Many-to-Many). The full article lifecycle "
            "follows: `draft` → `published` → `archived`.\n\n"
            "**Supported operations**\n\n"
            "| Method | Path | Description |\n"
            "|--------|------|-------------|\n"
            "| `GET` | `/api/v1/articles` | Paginated list with optional filters (B15) |\n"
            "| `GET` | `/api/v1/articles/{id}` | Fetch a single article by PK (B10) |\n"
            "| `PUT` | `/api/v1/articles/{id}` | Partial update (B12) |\n"
            "| `DELETE` | `/api/v1/articles/{id}` | Hard delete — 204 (B13) |"
        ),
        "externalDocs": {
            "description": "Article data model reference",
            "url": "https://github.com/SzoubineDev/adoptai-knowledgebaseapp#articles",
        },
    },
    {
        "name": "Applications",
        "description": (
            "Inventaire des **applications** (catalogue ServiceNow / logiciels Apple) "
            "avec criticité, source, département et indicateurs IAM dérivés."
        ),
    },
    {
        "name": "Data Sources",
        "description": "Comptages agrégés Apple, SAP, ServiceNow et HelpDesk.",
    },
    {
        "name": "Stats",
        "description": "Indicateurs IAM et réseau calculés à partir de l'inventaire.",
    },
    {
        "name": "Auth",
        "description": (
            "**Authentication & Identity** — JWT Bearer Token flow.\n\n"
            "| Method | Path | Description |\n"
            "|--------|------|-------------|\n"
            "| `POST` | `/api/v1/auth/register` | Create a new user account |\n"
            "| `POST` | `/api/v1/auth/login` | Obtain a JWT access token |\n"
            "| `GET`  | `/api/v1/auth/me` | Return the currently authenticated user (🔒 protected) |\n\n"
            "Tokens are signed HS256 JWTs. Include the token in every protected request:\n"
            "```\nAuthorization: Bearer <token>\n```"
        ),
    },
    {
        "name": "Health",
        "description": (
            "Infrastructure health and readiness probes.\n\n"
            "These endpoints are used by load balancers and monitoring systems "
            "to verify that the API process is running and reachable. "
            "The `/health` endpoint is intentionally lightweight and avoids "
            "any database call."
        ),
    },
]


# ---------------------------------------------------------------------------
# B26 — Professional Markdown description (rendered in Swagger UI & ReDoc)
# ---------------------------------------------------------------------------
API_DESCRIPTION: str = """
## AdoptAI App Knowledge Base API

A **centralized knowledge management system** built for AdoptAI to help
enterprise teams find, manage, and consume application guidance content.

### What this API provides

| Resource | Description |
|----------|-------------|
| **Articles** | Core content units: step-by-step guides, FAQs, how-tos for enterprise apps |
| **Categories** | Top-level taxonomy (SAP, ServiceNow, Apple MDM, …) |
| **Tags** | Cross-cutting keyword labels for fine-grained filtering |

### Versioning

All production endpoints are versioned under `/api/v1`.
Breaking changes will be introduced under a new version prefix (`/api/v2`, etc.).

### Authentication

This API uses **JWT Bearer Token** authentication.

1. Call `POST /api/v1/auth/register` to create an account.
2. Call `POST /api/v1/auth/login` to obtain a token.
3. Pass the token in the `Authorization` header on protected routes:

```
Authorization: Bearer <your_token>
```

Token lifetime is controlled by `ACCESS_TOKEN_EXPIRE_MINUTES` in `.env` (default: 30 min).

### Error format

Every error response follows a consistent JSON envelope — regardless of the
error source (validation, not found, conflict, internal):

```json
{
  "error": {
    "code":    "ARTICLE_NOT_FOUND",
    "message": "Article with id '42' was not found.",
    "status":  404
  }
}
```

| HTTP Status | Error code | Trigger |
|-------------|------------|---------|
| `404` | `ARTICLE_NOT_FOUND` | Requested article id does not exist |
| `409` | `ARTICLE_SLUG_CONFLICT` | New slug already used by another article |
| `422` | `REQUEST_VALIDATION_ERROR` | Invalid path/query parameter or body field |
| `500` | `INTERNAL_SERVER_ERROR` | Unexpected server-side failure |

### Project team

| Role | Name |
|------|------|
| Project supervisor | Khadija Boukhatem |
| Backend – Foundation & Core APIs | **Oussama** |
| Backend – Schemas & List Endpoints | Safouane |

### Source code

[github.com/SzoubineDev/adoptai-knowledgebaseapp](https://github.com/SzoubineDev/adoptai-knowledgebaseapp)
"""


# ---------------------------------------------------------------------------
# B2 — Lifespan: Prisma connect / disconnect
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Manages the Prisma client lifecycle.

    STARTUP : opens the connection pool to Supabase/PostgreSQL.
    SHUTDOWN: gracefully closes all active connections.
    """
    logger.info("Connecting to database via Prisma…")
    await prisma.connect()
    logger.info("Prisma connected ✓")

    yield  # ← application running

    logger.info("Disconnecting Prisma…")
    await prisma.disconnect()
    logger.info("Prisma disconnected ✓")


# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------
def create_application() -> FastAPI:
    """
    Builds and configures the FastAPI application instance.

    Using a factory function makes the app testable: tests can call
    `create_application()` with dependency overrides without importing
    the global `app` instance directly.
    """
    application = FastAPI(
        # ------------------------------------------------------------------
        # B26 — Core OpenAPI metadata
        # ------------------------------------------------------------------
        title=settings.PROJECT_NAME,
        version=settings.APP_VERSION,
        description=API_DESCRIPTION,
        # ------------------------------------------------------------------
        # B26 — Contact & license (rendered in the ReDoc sidebar)
        # ------------------------------------------------------------------
        contact={
            "name": "Oussama — Backend Developer",
            "url": "https://github.com/SzoubineDev/adoptai-knowledgebaseapp",
            "email": "oussamabaidi10@gmail.com",
        },
        license_info={
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT",
        },
        # ------------------------------------------------------------------
        # B26 — Tag definitions: labelled sections in Swagger UI
        # ------------------------------------------------------------------
        openapi_tags=OPENAPI_TAGS,
        # ------------------------------------------------------------------
        # B26 — Doc UI URLs (explicit for clarity)
        # ------------------------------------------------------------------
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        # ------------------------------------------------------------------
        # B26 — Swagger UI customisation for a polished developer experience
        # ------------------------------------------------------------------
        swagger_ui_parameters={
            "defaultModelsExpandDepth": 2,       # Expand schema models by default
            "defaultTagsExpandDepth": 1,         # Tags start expanded
            "operationsSorter": "method",        # Group by HTTP method
            "filter": True,                      # Search filter box visible
            "syntaxHighlight.theme": "monokai",  # Dark code highlighting
            "tryItOutEnabled": True,             # "Try it out" open by default
        },
        # Lifespan manages Prisma connect/disconnect (B2)
        lifespan=lifespan,
    )

    # ------------------------------------------------------------------
    # B2 — CORS Middleware
    # ------------------------------------------------------------------
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ------------------------------------------------------------------
    # B20 — Centralized exception handlers
    # ------------------------------------------------------------------
    register_exception_handlers(application)

    # ------------------------------------------------------------------
    # B10 — Versioned API router  (/api/v1/...)
    # ------------------------------------------------------------------
    application.include_router(api_router, prefix=settings.API_V1_STR)

    return application


# ---------------------------------------------------------------------------
# Module-level app instance (used by uvicorn, pytest, gunicorn)
# ---------------------------------------------------------------------------
app: FastAPI = create_application()


# ---------------------------------------------------------------------------
# B26 — Custom OpenAPI schema hook
# ---------------------------------------------------------------------------
# Overriding `app.openapi()` lets us inject additional metadata (servers,
# x-logo, security schemes) that FastAPI's default generator omits.
# The result is cached in `app.openapi_schema` after the first call.
# ---------------------------------------------------------------------------

def custom_openapi() -> dict:
    """
    Generate and cache a customised OpenAPI 3.1 schema.

    Called lazily on first access to /openapi.json. Subsequent requests
    are served from the in-memory cache (`app.openapi_schema`).
    """
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        contact=app.contact,            # type: ignore[arg-type]
        license_info=app.license_info,  # type: ignore[arg-type]
        tags=OPENAPI_TAGS,
        routes=app.routes,
    )

    # ------------------------------------------------------------------
    # B26 — x-logo extension (displayed in ReDoc header)
    # ------------------------------------------------------------------
    schema["info"]["x-logo"] = {
        "url": "https://avatars.githubusercontent.com/u/SzoubineDev",
        "altText": "AdoptAI Logo",
    }

    # ------------------------------------------------------------------
    # B26 — Servers block: documents environment URLs in Swagger UI
    # ------------------------------------------------------------------
    schema["servers"] = [
        {
            "url": "http://localhost:8000",
            "description": "Local development server",
        },
        {
            "url": "https://api.adoptai.example.com",
            "description": "Production server (placeholder — update before go-live)",
        },
    ]

    # ------------------------------------------------------------------
    # Auth Étape 4 — OAuth2 securitySchemes
    # ------------------------------------------------------------------
    # Injecting this block makes Swagger UI display the 🔒 padlock on
    # protected operations and enables the "Authorize" button to send
    # the Bearer token automatically in "Try it out" requests.
    # FastAPI generates the `security` array on each operation from the
    # OAuth2PasswordBearer declared in app/dependencies/auth.py, but the
    # top-level `securitySchemes` component must be present for ReDoc to
    # render the security section correctly.
    # ------------------------------------------------------------------
    schema.setdefault("components", {})
    schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "/api/v1/auth/login",
                    "scopes": {},
                }
            },
        }
    }

    app.openapi_schema = schema
    return app.openapi_schema


# Attach the custom schema generator to the app instance.
app.openapi = custom_openapi  # type: ignore[method-assign]


# ---------------------------------------------------------------------------
# Health-check endpoint
# ---------------------------------------------------------------------------
@app.get(
    "/health",
    tags=["Health"],
    summary="Liveness probe",
    description=(
        "Returns `200 OK` with basic application metadata.\n\n"
        "Used by load balancers and uptime monitors to verify the process is alive. "
        "This endpoint intentionally **avoids any database call** so it remains fast "
        "and reliable even when the database is temporarily unreachable.\n\n"
        "Use a separate **readiness** endpoint (future roadmap) to probe DB connectivity."
    ),
    response_description="Application is running and reachable.",
    responses={
        200: {
            "description": "API process is alive.",
            "content": {
                "application/json": {
                    "example": {
                        "status": "ok",
                        "app": "AdoptAI App Knowledge Base",
                        "version": "0.1.0",
                        "debug": False,
                        "api_prefix": "/api/v1",
                    }
                }
            },
        }
    },
)
def health_check() -> dict:
    """
    **Liveness probe** — confirms the API process is running.

    Returns application name, version, debug flag, and API prefix so
    infrastructure tools can verify they are hitting the correct service.
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
