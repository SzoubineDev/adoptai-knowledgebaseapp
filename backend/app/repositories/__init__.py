"""
repositories/__init__.py
Project : AdoptAI App Knowledge Base
Author  : Oussama
Stage   : 2 (Data Access)

Central export hub for all Prisma-based repositories.

These repositories are the ONLY data-access layer consumed by the
FastAPI endpoints (B10, B12, B13, B15). They use the Prisma async
client and replace the SQLAlchemy-based crud/ layer for the
knowledge-base entities (Article, Tag).

Usage:
    from app.repositories import article_repository, tag_repository
"""

from app.repositories.article_repository import ArticleRepository
from app.repositories.tag_repository import TagRepository

# ---------------------------------------------------------------------------
# Module-level singletons — stateless, safe to share across all requests.
# The Prisma client (connection) is passed in per-call via get_prisma().
# ---------------------------------------------------------------------------
article_repository: ArticleRepository = ArticleRepository()
tag_repository: TagRepository = TagRepository()

__all__ = [
    "ArticleRepository",
    "TagRepository",
    "article_repository",
    "tag_repository",
]
