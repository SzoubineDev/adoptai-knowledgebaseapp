"""
Auth Étape 4 - Authentication Endpoints
Project : AdoptAI App Knowledge Base
Author  : Oussama
Feature : Auth (Sécurité & Authentification)

Implements the three authentication routes mounted under /api/v1/auth:

  POST /api/v1/auth/register — Create a new user account
  POST /api/v1/auth/login    — Exchange credentials for a JWT access token
  GET  /api/v1/auth/me       — Return the currently authenticated user (🔒)

Design notes
------------
* POST /login uses `OAuth2PasswordRequestForm` (form-encoded body, not JSON)
  so the Swagger UI "Authorize" button works out of the box. The `username`
  field of the form is treated as the email address, which is standard
  OAuth2 practice.

* `sub` claim in the JWT is set to `str(user.id)` (integer PK as string),
  following the JWT RFC convention that `sub` is always a string.

* All 400/401 error responses follow the standard HTTPException format.
  (Not the custom AppBaseException envelope, since auth errors should remain
  framework-standard for interoperability with OAuth2 clients.)

* `hashed_password` is never present in any response — routes always
  return `UserResponse.model_validate(user)` which excludes that field.
"""

import logging
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.database import get_prisma
from app.core.security import create_access_token, get_password_hash, verify_password
from app.dependencies.auth import get_current_user
from app.schemas.user import Token, UserCreate, UserResponse
from app.core.config import settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Router — prefix "/auth" and tags applied in api/router.py
# ---------------------------------------------------------------------------
router = APIRouter(tags=["Auth"])


# ---------------------------------------------------------------------------
# POST /register  — Create a new user account
# ---------------------------------------------------------------------------

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description=(
        "Creates a new AdoptAI user account.\n\n"
        "**Validation flow**:\n"
        "1. Verify the email is not already registered → **400** if duplicate.\n"
        "2. Hash the plain-text password with bcrypt — never stored in clear text.\n"
        "3. Persist the new user to the database with default role `UTILISATEUR`.\n"
        "4. Return the created user profile (password excluded).\n\n"
        "> ℹ️ The role defaults to `UTILISATEUR`. "
        "An `ADMINISTRATEUR` must promote the account after registration."
    ),
    responses={
        201: {"description": "User account created successfully."},
        400: {
            "description": "Email address already registered.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Email already registered."
                    }
                }
            },
        },
    },
)
async def register(
    body: UserCreate,
    db=Depends(get_prisma),
) -> UserResponse:
    """
    **POST /api/v1/auth/register**

    Registers a new user account.

    - **email**: Must be unique. Validated as a proper email address.
    - **password**: Minimum 8 characters, must contain at least one digit.
      Stored as a bcrypt hash — never in plain text.
    - **nom** / **prenom**: Required identity fields.
    - **role**: Defaults to `UTILISATEUR` if not supplied.
    - **is_active**: Defaults to `True` — account is immediately usable.
    """
    logger.info("POST /auth/register — registration attempt for email=%r", body.email)

    # ------------------------------------------------------------------
    # Step 1: Uniqueness check — prevent duplicate email accounts
    # ------------------------------------------------------------------
    existing = await db.user.find_unique(where={"email": body.email})
    if existing is not None:
        logger.warning(
            "POST /auth/register — email %r already registered.", body.email
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered.",
        )

    # ------------------------------------------------------------------
    # Step 2: Hash the plain-text password (never stored in clear text)
    # ------------------------------------------------------------------
    hashed_pw = get_password_hash(body.password)

    # ------------------------------------------------------------------
    # Step 3: Persist the new user to the database
    # ------------------------------------------------------------------
    new_user = await db.user.create(
        data={
            "email":          body.email,
            "hashedPassword": hashed_pw,
            "nom":            body.nom,
            "prenom":         body.prenom,
            "role":           body.role.value,
            "isActive":       body.is_active,
        }
    )

    logger.info(
        "POST /auth/register — user created: id=%s email=%r role=%s",
        new_user.id, new_user.email, new_user.role,
    )

    # ------------------------------------------------------------------
    # Step 4: Return safe user profile (hashed_password excluded)
    # ------------------------------------------------------------------
    return UserResponse.model_validate(new_user)


# ---------------------------------------------------------------------------
# POST /login  — Exchange credentials for a JWT access token
# ---------------------------------------------------------------------------

@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Login and obtain a JWT access token",
    description=(
        "Authenticates a user and returns a signed JWT Bearer Token.\n\n"
        "**Request format**: `application/x-www-form-urlencoded` "
        "(standard OAuth2 Password flow — use `username` field for the email).\n\n"
        "**Validation flow**:\n"
        "1. Look up the user by email (`form_data.username`).\n"
        "2. Verify the password with bcrypt constant-time comparison.\n"
        "3. Check that the account is active.\n"
        "4. Sign and return a JWT access token.\n\n"
        "**Using the token**: Pass it in the `Authorization` header of "
        "every protected request:\n```\nAuthorization: Bearer <access_token>\n```\n\n"
        "> ℹ️ Click the 🔒 **Authorize** button at the top of Swagger UI "
        "to authenticate and test protected routes directly from the docs."
    ),
    responses={
        200: {"description": "Authentication successful — JWT token returned."},
        401: {
            "description": "Invalid credentials (user not found or wrong password).",
            "content": {
                "application/json": {
                    "example": {"detail": "Incorrect email or password."}
                }
            },
        },
        403: {
            "description": "Account is deactivated.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Inactive account. Please contact an administrator."
                    }
                }
            },
        },
    },
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db=Depends(get_prisma),
) -> Token:
    """
    **POST /api/v1/auth/login**

    Authenticates a user and returns a signed JWT access token.

    The request body must be `application/x-www-form-urlencoded` with:
    - **username**: The user's email address (OAuth2 convention).
    - **password**: The user's plain-text password.

    The returned `access_token` expires after `ACCESS_TOKEN_EXPIRE_MINUTES`
    minutes (default: 30). After expiry the client must log in again.
    """
    # Intentionally vague error message to prevent user enumeration attacks:
    # an attacker cannot distinguish "email not found" from "wrong password".
    _auth_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    logger.info(
        "POST /auth/login — login attempt for username=%r", form_data.username
    )

    # ------------------------------------------------------------------
    # Step 1: Look up user by email (OAuth2 uses `username` for the email)
    # ------------------------------------------------------------------
    user = await db.user.find_unique(where={"email": form_data.username})
    if user is None:
        logger.warning(
            "POST /auth/login — no user found for email=%r", form_data.username
        )
        raise _auth_error

    # ------------------------------------------------------------------
    # Step 2: Verify password (constant-time bcrypt comparison)
    # ------------------------------------------------------------------
    if not verify_password(form_data.password, user.hashedPassword):
        logger.warning(
            "POST /auth/login — wrong password for user id=%s email=%r",
            user.id, user.email,
        )
        raise _auth_error

    # ------------------------------------------------------------------
    # Step 3: Check account is active
    # ------------------------------------------------------------------
    if not user.isActive:
        logger.warning(
            "POST /auth/login — login denied: inactive account id=%s email=%r",
            user.id, user.email,
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive account. Please contact an administrator.",
        )

    # ------------------------------------------------------------------
    # Step 4: Create and return the JWT access token
    # sub = str(user.id)  ← JWT RFC: `sub` is always a string
    # role embedded for fast RBAC evaluation without extra DB round-trips
    # ------------------------------------------------------------------
    access_token = create_access_token(
        data={
            "sub":  str(user.id),
            "role": user.role,
        },
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    logger.info(
        "POST /auth/login — JWT issued for user id=%s email=%r role=%s",
        user.id, user.email, user.role,
    )

    return Token(access_token=access_token, token_type="bearer")


# ---------------------------------------------------------------------------
# GET /me  — Return the currently authenticated user (protected route)
# ---------------------------------------------------------------------------

@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current authenticated user",
    description=(
        "Returns the profile of the currently authenticated user.\n\n"
        "🔒 **Protected** — requires a valid `Authorization: Bearer <token>` header.\n\n"
        "The response includes all profile fields except the hashed password. "
        "Use this endpoint to verify a token is still valid and to retrieve "
        "the user's current role after a role change by an administrator."
    ),
    responses={
        200: {"description": "Current user profile returned successfully."},
        401: {
            "description": "Token missing, malformed, expired, or user deleted.",
            "content": {
                "application/json": {
                    "example": {"detail": "Could not validate credentials."}
                }
            },
        },
        403: {
            "description": "Account has been deactivated.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Inactive account. Please contact an administrator."
                    }
                }
            },
        },
    },
)
async def me(
    current_user=Depends(get_current_user),
) -> UserResponse:
    """
    **GET /api/v1/auth/me**

    Returns the profile of the currently authenticated user.

    The `get_current_user` dependency (injected via `Depends`) handles all
    token validation steps:
      1. Extracts and verifies the Bearer JWT.
      2. Looks up the user in the database.
      3. Checks the account is active.

    This handler only needs to serialise the result.
    """
    logger.info(
        "GET /auth/me — returning profile for user id=%s email=%r",
        current_user.id, current_user.email,
    )
    return UserResponse.model_validate(current_user)
