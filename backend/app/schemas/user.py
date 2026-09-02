"""
Auth Étape 2 - User Pydantic Schemas
Project : AdoptAI App Knowledge Base
Author  : Oussama
Feature : Auth (Sécurité & Authentification)

Defines all Pydantic v2 request/response schemas for the User entity and
the JWT authentication flow.

Schema hierarchy
----------------
  UserBase          — shared validated fields (email, nom, prenom, role, is_active)
    └── UserCreate  — registration payload (adds plain-text `password`)
  UserLogin         — login payload (email + password only)
  UserResponse      — API response (adds id, created_at; NEVER exposes password)
  Token             — JWT response returned on successful login
  TokenData         — internal type for decoded JWT payload (used in auth.py)

Security invariant
------------------
`hashed_password` is NEVER present in any response schema.
The only schema that accepts a plain-text password is `UserCreate`,
and it is consumed immediately by `core/security.py → get_password_hash()`
before anything is written to the database.

RBAC
----
`RoleEnum` mirrors the Prisma enum `RoleEnum` in `schema.prisma`.
Both must be kept in sync. Adding a new role requires:
  1. Updating this enum.
  2. Adding the value to schema.prisma's RoleEnum.
  3. Running `prisma migrate dev`.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator


# ---------------------------------------------------------------------------
# RBAC Enum — mirrors schema.prisma RoleEnum
# ---------------------------------------------------------------------------

class RoleEnum(str, Enum):
    """
    Role-Based Access Control levels for AdoptAI users.

    Hierarchy (highest → lowest privilege):
        ADMINISTRATEUR  — full system access, user management
        RESPONSABLE_IT  — can manage articles, categories, tags, and applications
        AGENT_HELPDESK  — can read all content and manage their own tickets
        UTILISATEUR     — read-only access to published articles
    """
    ADMINISTRATEUR = "ADMINISTRATEUR"
    RESPONSABLE_IT = "RESPONSABLE_IT"
    AGENT_HELPDESK = "AGENT_HELPDESK"
    UTILISATEUR    = "UTILISATEUR"


# ---------------------------------------------------------------------------
# Base schema — shared fields for all User schemas
# ---------------------------------------------------------------------------

class UserBase(BaseModel):
    """
    Common validated fields shared by UserCreate and UserResponse.

    Not used directly in API endpoints — serves as the base class only.
    """

    email: EmailStr = Field(
        ...,
        description=(
            "User's email address. Used as the unique login identifier. "
            "Must be a valid email format (validated by email-validator)."
        ),
        examples=["oussama@adoptai.fr"],
    )

    nom: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="User's family name (nom de famille).",
        examples=["Baidi"],
    )

    prenom: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="User's given name (prénom).",
        examples=["Oussama"],
    )

    role: RoleEnum = Field(
        default=RoleEnum.UTILISATEUR,
        description=(
            "User's RBAC role. Determines which resources and operations are "
            "accessible. Defaults to UTILISATEUR (least privileged)."
        ),
        examples=[RoleEnum.RESPONSABLE_IT],
    )

    is_active: bool = Field(
        default=True,
        description=(
            "Whether the account is active. Inactive accounts cannot log in. "
            "Can only be set to False by an ADMINISTRATEUR."
        ),
        examples=[True],
    )


# ---------------------------------------------------------------------------
# UserCreate — registration payload (plain-text password accepted here only)
# ---------------------------------------------------------------------------

class UserCreate(UserBase):
    """
    Payload for POST /api/v1/auth/register.

    Extends UserBase with a plain-text password field.
    The password is validated here (length, complexity) and then
    immediately hashed in the route handler via `get_password_hash()`.

    SECURITY: `password` is write-only — it NEVER appears in any response.
    """

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description=(
            "Plain-text password for the new account. "
            "Must be at least 8 characters. "
            "Will be bcrypt-hashed before storage — never stored in plain text."
        ),
        examples=["Str0ng!P@ssword"],
    )

    @field_validator("password")
    @classmethod
    def password_must_contain_digit(cls, v: str) -> str:
        """
        Enforce a minimal complexity rule: password must contain at least
        one digit. More complex rules (uppercase, special char) can be added
        here without touching the route handler.
        """
        if not any(c.isdigit() for c in v):
            raise ValueError("Le mot de passe doit contenir au moins un chiffre.")
        return v

    model_config = {"json_schema_extra": {"exclude": {"password"}}}


# ---------------------------------------------------------------------------
# UserLogin — login payload
# ---------------------------------------------------------------------------

class UserLogin(BaseModel):
    """
    Payload for POST /api/v1/auth/login.

    Intentionally minimal — only the credentials needed to authenticate.
    Does not inherit from UserBase to avoid exposing optional fields.
    """

    email: EmailStr = Field(
        ...,
        description="Email address of the account to log into.",
        examples=["oussama@adoptai.fr"],
    )

    password: str = Field(
        ...,
        min_length=1,
        description="Plain-text password for the account.",
        examples=["Str0ng!P@ssword"],
    )


# ---------------------------------------------------------------------------
# UserResponse — safe API response (NEVER exposes hashed_password)
# ---------------------------------------------------------------------------

class UserResponse(UserBase):
    """
    Response schema for authenticated user data.

    Returned by:
      - POST /api/v1/auth/register  (201 Created)
      - GET  /api/v1/auth/me        (200 OK)

    SECURITY INVARIANT:
      - `hashed_password` is ABSENT from this schema and will never be
        serialised, regardless of what the Prisma model contains.
      - `from_attributes=True` enables Pydantic v2 to read directly from
        Prisma model instances (ORM mode).

    Field mapping note:
      Prisma stores `hashedPassword` (camelCase) mapped to `hashed_password`
      (snake_case, @map). UserResponse uses snake_case to match Python
      conventions and Prisma's Python client output.
    """

    id: int = Field(
        ...,
        description="Unique numeric primary key assigned by the database.",
        examples=[1],
    )

    created_at: datetime = Field(
        ...,
        description=(
            "ISO 8601 timestamp of account creation. "
            "Set automatically by the database at INSERT time."
        ),
        examples=["2026-09-02T16:00:00Z"],
    )

    model_config = {
        # ORM mode: allows `UserResponse.model_validate(prisma_user_object)`
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "email": "oussama@adoptai.fr",
                "nom": "Baidi",
                "prenom": "Oussama",
                "role": "RESPONSABLE_IT",
                "is_active": True,
                "created_at": "2026-09-02T16:00:00Z",
            }
        },
    }


# ---------------------------------------------------------------------------
# Token — JWT response returned on successful login
# ---------------------------------------------------------------------------

class Token(BaseModel):
    """
    Response schema for POST /api/v1/auth/login.

    Contains the signed JWT access token and its type so the frontend
    can store it and include it in subsequent `Authorization: Bearer <token>`
    headers.
    """

    access_token: str = Field(
        ...,
        description=(
            "Signed JWT access token. Include this in the `Authorization` "
            "header of every protected request: `Bearer <access_token>`."
        ),
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."],
    )

    token_type: str = Field(
        default="bearer",
        description=(
            "Token scheme. Always `bearer` for OAuth2 / JWT flows. "
            "The frontend should prefix the token with `Bearer ` in the header."
        ),
        examples=["bearer"],
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzI1Mjk0MDAwfQ.signature",
                "token_type": "bearer",
            }
        }
    }


# ---------------------------------------------------------------------------
# TokenData — internal decoded JWT payload (used in app/dependencies/auth.py)
# ---------------------------------------------------------------------------

class TokenData(BaseModel):
    """
    Internal schema representing the decoded payload of a JWT access token.

    NOT exposed via any API endpoint — used exclusively by `get_current_user()`
    in `app/dependencies/auth.py` to carry the validated user id after
    `verify_token()` decodes the JWT.

    Fields
    ------
    user_id : The `sub` claim from the JWT, cast to int.
               Used to fetch the full User record from the database.
    role    : The `role` claim embedded in the token for fast RBAC checks
              without an extra DB round-trip in simple middleware.
    """

    user_id: Optional[int] = Field(
        default=None,
        description="Numeric user id extracted from the JWT `sub` claim.",
    )

    role: Optional[RoleEnum] = Field(
        default=None,
        description="User role embedded in the JWT for fast RBAC evaluation.",
    )
