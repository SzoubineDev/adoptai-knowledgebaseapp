"""
schemas/__init__.py
Project : AdoptAI App Knowledge Base
Author  : Oussama
Stage   : 1 (Foundation), Feature Auth

Central import hub for all Pydantic v2 schemas.
Importing from this module gives access to all request/response models.

Usage:
    from app.schemas import ArticleResponse, ArticleCreate, ArticleUpdate
    from app.schemas import CategoryResponse, CategoryCreate, CategoryUpdate
    from app.schemas import TagResponse, TagCreate, TagUpdate
    from app.schemas import UserCreate, UserResponse, Token, RoleEnum
"""

# Category schemas (B4)
from app.schemas.category import (  # noqa: F401
    CategoryBase,
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
)

# Tag schemas (B5)
from app.schemas.tag import (  # noqa: F401
    TagBase,
    TagCreate,
    TagUpdate,
    TagResponse,
)

# Article schemas (B3) — imported last because ArticleResponse
# depends on CategoryResponse and TagResponse above.
from app.schemas.article import (  # noqa: F401
    ArticleStatus,
    TypeHebergement,
    ArticleBase,
    ArticleCreate,
    ArticleUpdate,
    ArticleResponse,
)

# User schemas (Feature Auth — Oussama)
from app.schemas.user import (  # noqa: F401
    RoleEnum,
    UserBase,
    UserCreate,
    UserLogin,
    UserResponse,
    Token,
    TokenData,
)

__all__ = [
    # Category
    "CategoryBase",
    "CategoryCreate",
    "CategoryUpdate",
    "CategoryResponse",
    # Tag
    "TagBase",
    "TagCreate",
    "TagUpdate",
    "TagResponse",
    # Article
    "ArticleStatus",
    "TypeHebergement",
    "ArticleBase",
    "ArticleCreate",
    "ArticleUpdate",
    "ArticleResponse",
    # User / Auth
    "RoleEnum",
    "UserBase",
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "Token",
    "TokenData",
]
