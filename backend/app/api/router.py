"""
API Router – aggregates all endpoint sub-routers
Project : AdoptAI App Knowledge Base
Author  : Oussama
Stages  : 3 (Core APIs & Errors), Feature Auth (Étape 4)

All versioned API routers are registered here and mounted with their
respective URL prefixes. `main.py` imports `api_router` and includes it
once under the global `/api/v1` prefix defined in settings.API_V1_STR.

Final URL structure:
  /api/v1/auth/register     ← Auth — POST  (register)
  /api/v1/auth/login        ← Auth — POST  (login / token)
  /api/v1/auth/me           ← Auth — GET   (current user, protected)
  /api/v1/articles/         ← Articles — GET list (B15)
  /api/v1/articles/{id}     ← Articles — GET, PUT, DELETE (B10, B12, B13)

Adding a new endpoint module requires only two lines:
    from app.api.endpoints.foo import router as foo_router
    api_router.include_router(foo_router, prefix="/foo")
"""

from fastapi import APIRouter

from app.api.endpoints.articles import router as articles_router
from app.api.endpoints.auth import router as auth_router
from app.api.endpoints.inventory import router as inventory_router

api_router = APIRouter()

# ------------------------------------------------------------------
# Auth routes — /api/v1/auth/{register,login,me}
# Mounted first so token-related 401 responses appear before
# resource-level 404s in the OpenAPI operation list.
# ------------------------------------------------------------------
api_router.include_router(auth_router, prefix="/auth")

# ------------------------------------------------------------------
# Knowledge-base resource routes
# ------------------------------------------------------------------
api_router.include_router(articles_router, prefix="/articles")
api_router.include_router(inventory_router)
