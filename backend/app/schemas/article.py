"""
B3 - Pydantic Schemas for Article
Project : AdoptAI App Knowledge Base
Author  : Oussama
Stage   : 1 (Foundation)

Defines the full Pydantic v2 schema set for the Article resource.
Articles are the central entity of the knowledge base:
  - They belong to one Category (nullable FK)
  - They carry many Tags (Many-to-Many via article_tags)
  - They expose a `type_hebergement` field for hosting context

Schema hierarchy:
    ArticleStatus      – str Enum: draft | published | archived
    ArticleBase        – shared validated fields
    ├── ArticleCreate  – body for POST /articles
    ├── ArticleUpdate  – body for PUT /articles/{id}  (all fields optional)
    └── ArticleResponse – full API response with nested Category + Tags
"""

import enum
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.schemas.category import CategoryResponse
from app.schemas.tag import TagResponse


# ---------------------------------------------------------------------------
# B3 — ArticleStatus Enum
# ---------------------------------------------------------------------------
class ArticleStatus(str, enum.Enum):
    """
    Lifecycle state of an article.

    Using `str` as a mixin makes the enum JSON-serialisable by default
    (FastAPI will emit the string value, not the Enum name).

    draft     – Work-in-progress; not visible to end users.
    published – Approved and live in the knowledge base.
    archived  – Removed from active listings but preserved for audit history.
    """

    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


# ---------------------------------------------------------------------------
# B3 — TypeHebergement Enum
# ---------------------------------------------------------------------------
class TypeHebergement(str, enum.Enum):
    """
    Hosting/deployment context of the application described in the article.

    cloud     – Fully cloud-hosted (SaaS / IaaS).
    on_premise – Deployed on the organisation's own infrastructure.
    hybride   – Mix of cloud and on-premise.
    """

    CLOUD = "cloud"
    ON_PREMISE = "on_premise"
    HYBRIDE = "hybride"


# ---------------------------------------------------------------------------
# B3 — ArticleBase
# ---------------------------------------------------------------------------
class ArticleBase(BaseModel):
    """
    Shared fields used by both Create and Update schemas.

    Constraints mirror the ORM column definitions:
        title   → String(255)
        slug    → String(300), URL-safe pattern
        content → Text (no max length enforced at the API layer)
        status  → ArticleStatus enum (default: draft)
        type_hebergement → TypeHebergement enum (optional)
        category_id      → nullable FK
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Article headline (max 255 characters).",
        examples=["How to reset your SAP password"],
    )
    slug: str = Field(
        ...,
        min_length=1,
        max_length=300,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
        description=(
            "URL-safe unique identifier — lowercase letters, digits, "
            "and hyphens only (e.g., 'how-to-reset-sap-password')."
        ),
        examples=["how-to-reset-sap-password"],
    )
    content: str = Field(
        ...,
        min_length=1,
        description="Full article body (plain text or Markdown).",
        examples=["## Step 1\nNavigate to the SAP login page and click 'Forgot password'."],
    )
    status: ArticleStatus = Field(
        default=ArticleStatus.DRAFT,
        description="Article lifecycle state (draft | published | archived).",
        examples=["draft"],
    )
    type_hebergement: Optional[TypeHebergement] = Field(
        default=None,
        description=(
            "Hosting context of the application described in this article "
            "(cloud | on_premise | hybride). Null if not applicable."
        ),
        examples=["cloud"],
    )
    category_id: Optional[int] = Field(
        default=None,
        ge=1,
        description="FK to the owning Category. Null means the article is uncategorised.",
        examples=[1],
    )

    # ------------------------------------------------------------------
    # Field validators
    # ------------------------------------------------------------------
    @field_validator("slug", mode="before")
    @classmethod
    def normalize_slug(cls, value: str) -> str:
        """Strips whitespace and lowercases the slug."""
        return value.strip().lower()

    @field_validator("title", "content", mode="before")
    @classmethod
    def strip_text_fields(cls, value: str) -> str:
        """Strips surrounding whitespace from text fields."""
        return value.strip()

    @field_validator("status", mode="before")
    @classmethod
    def normalize_status(cls, value: str | ArticleStatus) -> ArticleStatus:
        """Accepts both the enum member and its string value."""
        if isinstance(value, ArticleStatus):
            return value
        return ArticleStatus(value.lower())


# ---------------------------------------------------------------------------
# B3 — ArticleCreate  (POST /articles)
# ---------------------------------------------------------------------------
class ArticleCreate(ArticleBase):
    """
    Request body for creating a new Article.

    Inherits all validated fields from ArticleBase and adds `tag_ids`
    so the caller can associate tags at creation time.
    The `id` and timestamps are assigned by the database on INSERT.
    """

    tag_ids: List[int] = Field(
        default_factory=list,
        description="List of Tag IDs to associate with the new article.",
        examples=[[1, 3]],
    )

    @field_validator("tag_ids", mode="before")
    @classmethod
    def deduplicate_tag_ids(cls, value: List[int]) -> List[int]:
        """Removes duplicate tag IDs while preserving insertion order."""
        seen: set[int] = set()
        return [tag_id for tag_id in value if not (tag_id in seen or seen.add(tag_id))]  # type: ignore[func-returns-value]


# ---------------------------------------------------------------------------
# B3 — ArticleUpdate  (PUT /articles/{id})
# ---------------------------------------------------------------------------
class ArticleUpdate(BaseModel):
    """
    Request body for updating an existing Article.

    ALL fields are optional to support partial updates (PATCH semantics
    delivered via PUT). Only the fields explicitly supplied in the request
    body are forwarded to the repository's update() method.

    `tag_ids`, when provided, **replaces** the current tag set entirely
    (full replacement strategy, not additive). Pass an empty list [] to
    remove all tags.
    """

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="New article headline.",
        examples=["Updated: How to reset your SAP password"],
    )
    slug: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=300,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
        description="New URL-safe slug.",
        examples=["updated-how-to-reset-sap-password"],
    )
    content: Optional[str] = Field(
        default=None,
        min_length=1,
        description="New article body (plain text or Markdown).",
    )
    status: Optional[ArticleStatus] = Field(
        default=None,
        description="New lifecycle state.",
        examples=["published"],
    )
    type_hebergement: Optional[TypeHebergement] = Field(
        default=None,
        description="New hosting context.",
        examples=["on_premise"],
    )
    category_id: Optional[int] = Field(
        default=None,
        ge=1,
        description="New category FK. Pass null to un-categorise the article.",
    )
    tag_ids: Optional[List[int]] = Field(
        default=None,
        description=(
            "Full replacement list of Tag IDs. "
            "Pass [] to remove all tags; omit to leave tags unchanged."
        ),
        examples=[[2, 4]],
    )

    # ------------------------------------------------------------------
    # Field validators
    # ------------------------------------------------------------------
    @field_validator("slug", mode="before")
    @classmethod
    def normalize_slug(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        return value.strip().lower()

    @field_validator("title", "content", mode="before")
    @classmethod
    def strip_text_fields(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        return value.strip()

    @field_validator("status", mode="before")
    @classmethod
    def normalize_status(cls, value: Optional[str | ArticleStatus]) -> Optional[ArticleStatus]:
        if value is None:
            return None
        if isinstance(value, ArticleStatus):
            return value
        return ArticleStatus(value.lower())

    @field_validator("tag_ids", mode="before")
    @classmethod
    def deduplicate_tag_ids(cls, value: Optional[List[int]]) -> Optional[List[int]]:
        if value is None:
            return None
        seen: set[int] = set()
        return [tag_id for tag_id in value if not (tag_id in seen or seen.add(tag_id))]  # type: ignore[func-returns-value]

    @model_validator(mode="after")
    def at_least_one_field(self) -> "ArticleUpdate":
        """Ensures the client sends at least one field to update."""
        provided = {
            k: v for k, v in self.model_dump(exclude_unset=True).items()
            if v is not None
        }
        if not provided:
            raise ValueError(
                "At least one field must be provided for an update."
            )
        return self


# ---------------------------------------------------------------------------
# B3 — ArticleResponse  (GET /articles/{id}, PUT /articles/{id}, …)
# ---------------------------------------------------------------------------
class ArticleResponse(ArticleBase):
    """
    Full API response shape for an Article.

    Extends ArticleBase with:
    - Server-assigned fields: id, created_at, updated_at.
    - Nested related objects: category (CategoryResponse), tags (List[TagResponse]).

    `from_attributes=True` enables direct construction from a SQLAlchemy ORM
    instance or a Prisma model object (replaces Pydantic v1's `orm_mode=True`).
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Auto-incremented primary key.", examples=[42])
    category: Optional[CategoryResponse] = Field(
        default=None,
        description="Nested Category object (null if the article is uncategorised).",
    )
    tags: List[TagResponse] = Field(
        default_factory=list,
        description="List of Tags associated with this article.",
    )
    created_at: datetime = Field(
        ...,
        description="UTC timestamp of article creation.",
    )
    updated_at: datetime = Field(
        ...,
        description="UTC timestamp of last update.",
    )
