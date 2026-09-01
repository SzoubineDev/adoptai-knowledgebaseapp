"""
B4 - Pydantic Schemas for Category
Project : AdoptAI App Knowledge Base
Author  : Oussama
Stage   : 1 (Foundation)

Defines the full Pydantic v2 schema set for the Category resource.
These schemas are used exclusively by FastAPI for request validation
and response serialisation — they are independent of the ORM layer.

Schema hierarchy:
    CategoryBase        – shared read/write fields
    ├── CategoryCreate  – body for POST /categories
    ├── CategoryUpdate  – body for PUT /categories/{id}  (all fields optional)
    └── CategoryResponse – API response shape (includes id + timestamps)
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ---------------------------------------------------------------------------
# B4 — CategoryBase
# ---------------------------------------------------------------------------
class CategoryBase(BaseModel):
    """
    Shared fields used by both Create and Update schemas.

    `name` and `slug` are required at the base level and carry
    length constraints that mirror the database column definitions
    in the ORM model (String(100) / String(120)).
    """

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Human-readable category label (e.g., 'SAP', 'ServiceNow').",
        examples=["SAP"],
    )
    slug: str = Field(
        ...,
        min_length=1,
        max_length=120,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
        description=(
            "URL-safe unique identifier — lowercase letters, digits, "
            "and hyphens only (e.g., 'service-now')."
        ),
        examples=["sap"],
    )
    description: Optional[str] = Field(
        default=None,
        description="Optional long-form description of the category.",
        examples=["All articles related to the SAP ERP ecosystem."],
    )

    @field_validator("slug", mode="before")
    @classmethod
    def normalize_slug(cls, value: str) -> str:
        """Strips surrounding whitespace and lowercases the slug."""
        return value.strip().lower()


# ---------------------------------------------------------------------------
# B4 — CategoryCreate  (POST /categories)
# ---------------------------------------------------------------------------
class CategoryCreate(CategoryBase):
    """
    Request body for creating a new Category.

    Inherits all fields from CategoryBase. No extra fields are required
    at creation time — `id` and timestamps are assigned by the database.
    """
    pass


# ---------------------------------------------------------------------------
# B4 — CategoryUpdate  (PUT /categories/{id})
# ---------------------------------------------------------------------------
class CategoryUpdate(BaseModel):
    """
    Request body for updating an existing Category.

    ALL fields are optional to support partial updates (PATCH semantics
    delivered via PUT). Only provided fields are forwarded to the repository.
    """

    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="New human-readable category label.",
        examples=["ServiceNow"],
    )
    slug: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=120,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
        description="New URL-safe slug.",
        examples=["service-now"],
    )
    description: Optional[str] = Field(
        default=None,
        description="New description, or null to clear it.",
    )

    @field_validator("slug", mode="before")
    @classmethod
    def normalize_slug(cls, value: Optional[str]) -> Optional[str]:
        """Strips whitespace and lowercases the slug when provided."""
        if value is None:
            return None
        return value.strip().lower()


# ---------------------------------------------------------------------------
# B4 — CategoryResponse  (GET /categories, GET /categories/{id}, …)
# ---------------------------------------------------------------------------
class CategoryResponse(CategoryBase):
    """
    Full API response shape for a Category.

    Extends CategoryBase with server-assigned fields (id, timestamps).
    `from_attributes=True` enables direct construction from a SQLAlchemy
    ORM instance or a Prisma model object.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Auto-incremented primary key.", examples=[1])
    created_at: datetime = Field(
        ...,
        description="UTC timestamp of category creation.",
    )
    updated_at: datetime = Field(
        ...,
        description="UTC timestamp of last update.",
    )
