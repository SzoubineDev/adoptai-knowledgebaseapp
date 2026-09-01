"""
B5 - Pydantic Schemas for Tag
Project : AdoptAI App Knowledge Base
Author  : Oussama
Stage   : 1 (Foundation)

Defines the full Pydantic v2 schema set for the Tag resource.
Tags implement a Many-to-Many relationship with Articles.

Schema hierarchy:
    TagBase        – shared read/write fields
    ├── TagCreate  – body for POST /tags
    ├── TagUpdate  – body for PUT /tags/{id}  (all fields optional)
    └── TagResponse – API response shape (includes id + created_at)
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ---------------------------------------------------------------------------
# B5 — TagBase
# ---------------------------------------------------------------------------
class TagBase(BaseModel):
    """
    Shared fields used by both Create and Update schemas.

    Length constraints mirror the ORM column definitions:
        name → String(80)
        slug → String(100)
    """

    name: str = Field(
        ...,
        min_length=1,
        max_length=80,
        description="Unique human-readable tag label (e.g., 'Python', 'SAP-FICO').",
        examples=["SAP-FICO"],
    )
    slug: str = Field(
        ...,
        min_length=1,
        max_length=100,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
        description=(
            "URL-safe unique identifier — lowercase letters, digits, "
            "and hyphens only (e.g., 'sap-fico')."
        ),
        examples=["sap-fico"],
    )

    @field_validator("slug", mode="before")
    @classmethod
    def normalize_slug(cls, value: str) -> str:
        """Strips surrounding whitespace and lowercases the slug."""
        return value.strip().lower()

    @field_validator("name", mode="before")
    @classmethod
    def strip_name(cls, value: str) -> str:
        """Strips surrounding whitespace from the tag name."""
        return value.strip()


# ---------------------------------------------------------------------------
# B5 — TagCreate  (POST /tags)
# ---------------------------------------------------------------------------
class TagCreate(TagBase):
    """
    Request body for creating a new Tag.

    Inherits all validated fields from TagBase. The `id` and `created_at`
    are assigned by the database on INSERT.
    """
    pass


# ---------------------------------------------------------------------------
# B5 — TagUpdate  (PUT /tags/{id})
# ---------------------------------------------------------------------------
class TagUpdate(BaseModel):
    """
    Request body for updating an existing Tag.

    ALL fields are optional to support partial updates. Only the fields
    explicitly provided in the request body will be modified.
    """

    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=80,
        description="New tag label.",
        examples=["SAP-CO"],
    )
    slug: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
        description="New URL-safe slug.",
        examples=["sap-co"],
    )

    @field_validator("slug", mode="before")
    @classmethod
    def normalize_slug(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        return value.strip().lower()

    @field_validator("name", mode="before")
    @classmethod
    def strip_name(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        return value.strip()


# ---------------------------------------------------------------------------
# B5 — TagResponse  (GET /tags, GET /tags/{id}, nested in ArticleResponse)
# ---------------------------------------------------------------------------
class TagResponse(TagBase):
    """
    Full API response shape for a Tag.

    Extends TagBase with server-assigned fields (id, created_at).
    Note: Tags do NOT have an `updated_at` column in the ORM model;
    tags are immutable once created (name/slug updates replace the tag).

    `from_attributes=True` enables construction from ORM / Prisma objects.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Auto-incremented primary key.", examples=[1])
    created_at: datetime = Field(
        ...,
        description="UTC timestamp of tag creation (set by the database server).",
    )
