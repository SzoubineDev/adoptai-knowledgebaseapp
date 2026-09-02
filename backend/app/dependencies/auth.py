"""
Auth Étape 3 - Authentication Dependency
Project : AdoptAI App Knowledge Base
Author  : Oussama
Feature : Auth (Sécurité & Authentification)

This module exposes the `get_current_user` FastAPI dependency and its
companion `require_role` factory — the two building blocks for protecting
any route in the application.

How it fits in the request pipeline
-------------------------------------
  1. Client sends: ``Authorization: Bearer <jwt_token>``
  2. FastAPI extracts the token via `OAuth2PasswordBearer` (oauth2_scheme).
  3. `get_current_user` decodes + validates the JWT with `decode_access_token`.
  4. It fetches the full User record from Prisma to verify the account
     still exists and is active.
  5. The route handler receives the authenticated `User` object directly.

Error responses (all 401 Unauthorized)
---------------------------------------
  CREDENTIALS_EXCEPTION  — token missing / malformed / expired / bad signature
  USER_NOT_FOUND         — valid token but user deleted from DB after issue
  INACTIVE_USER          — valid token + user exists but `is_active` is False
  (403 Forbidden)        — valid token + active user but insufficient role

Usage
------
  from app.dependencies.auth import get_current_user, require_role
  from app.schemas.user import RoleEnum

  # Protect a route — any authenticated user:
  @router.get("/me")
  async def me(current_user = Depends(get_current_user)):
      return current_user

  # Protect a route — RESPONSABLE_IT or above only:
  @router.delete("/articles/{id}")
  async def delete_article(
      article_id: int,
      _: User = Depends(require_role(RoleEnum.RESPONSABLE_IT)),
  ):
      ...
"""

import logging
from typing import List

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from app.core.database import get_prisma
from app.core.security import decode_access_token
from app.schemas.user import RoleEnum, TokenData

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# OAuth2 scheme — tells FastAPI (and Swagger UI) where to get the token
# ---------------------------------------------------------------------------
# `tokenUrl` points to the login endpoint so Swagger UI's "Authorize" button
# works out of the box without any extra configuration.
# The full path must match the one registered in api/router.py.
# ---------------------------------------------------------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# ---------------------------------------------------------------------------
# Reusable 401 exception (avoids repeating the same dict across the module)
# ---------------------------------------------------------------------------
_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials.",
    headers={"WWW-Authenticate": "Bearer"},
)


# ---------------------------------------------------------------------------
# get_current_user — core auth dependency
# ---------------------------------------------------------------------------

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db=Depends(get_prisma),
):
    """
    FastAPI dependency that validates the Bearer token and returns the
    authenticated Prisma User model.

    Steps
    -----
    1. Decode the JWT with `decode_access_token()` from `core/security.py`.
       Raises `_CREDENTIALS_EXCEPTION` (401) if the token is malformed,
       expired, or the signature is invalid.

    2. Extract the `sub` claim (user id) and `role` claim from the payload.
       Raises `_CREDENTIALS_EXCEPTION` if `sub` is missing or not a valid int.

    3. Fetch the User from Prisma by primary key.
       Raises HTTP 401 with detail "User not found." if the account was
       deleted after the token was issued.

    4. Check `user.is_active`.
       Raises HTTP 403 (Forbidden) with detail "Inactive account." if the
       account has been deactivated by an administrator.

    Returns
    -------
    prisma.models.User
        The full Prisma User object (includes all fields except those
        excluded by the ORM — hashed_password IS present here in the
        server-side object, but is NEVER serialised into any response
        because the route handlers use `UserResponse.model_validate(user)`).

    Typical usage in a route
    ------------------------
        from app.dependencies.auth import get_current_user
        from prisma.models import User

        @router.get("/me", response_model=UserResponse)
        async def me(current_user: User = Depends(get_current_user)):
            return UserResponse.model_validate(current_user)
    """
    # ----------------------------------------------------------------
    # Step 1: Decode and verify the JWT signature + expiry
    # ----------------------------------------------------------------
    try:
        payload = decode_access_token(token)
    except JWTError as exc:
        logger.warning("JWT decode failed: %s", exc)
        raise _CREDENTIALS_EXCEPTION from exc

    # ----------------------------------------------------------------
    # Step 2: Extract and validate the `sub` (user id) claim
    # ----------------------------------------------------------------
    sub: str | None = payload.get("sub")
    if sub is None:
        logger.warning("JWT payload missing 'sub' claim.")
        raise _CREDENTIALS_EXCEPTION

    try:
        user_id = int(sub)
    except (ValueError, TypeError):
        logger.warning("JWT 'sub' claim is not a valid integer: %r", sub)
        raise _CREDENTIALS_EXCEPTION

    role_str: str | None = payload.get("role")
    token_data = TokenData(
        user_id=user_id,
        role=RoleEnum(role_str) if role_str else None,
    )

    # ----------------------------------------------------------------
    # Step 3: Fetch the user from the database
    # ----------------------------------------------------------------
    user = await db.user.find_unique(where={"id": token_data.user_id})

    if user is None:
        logger.warning(
            "JWT references user id=%s which no longer exists in the DB.",
            token_data.user_id,
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # ----------------------------------------------------------------
    # Step 4: Check the account is still active
    # ----------------------------------------------------------------
    if not user.isActive:
        logger.warning(
            "Login attempt by inactive user id=%s email=%r.",
            user.id,
            user.email,
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive account. Please contact an administrator.",
        )

    logger.debug(
        "Authenticated user id=%s email=%r role=%s",
        user.id, user.email, user.role,
    )
    return user


# ---------------------------------------------------------------------------
# require_role — RBAC factory dependency
# ---------------------------------------------------------------------------

# Role hierarchy for comparison (index = privilege level, higher = more powerful)
_ROLE_HIERARCHY: List[RoleEnum] = [
    RoleEnum.UTILISATEUR,
    RoleEnum.AGENT_HELPDESK,
    RoleEnum.RESPONSABLE_IT,
    RoleEnum.ADMINISTRATEUR,
]


def require_role(minimum_role: RoleEnum):
    """
    Factory that returns a FastAPI dependency enforcing a minimum RBAC role.

    Designed to be used with `Depends()` in route signatures. The returned
    dependency calls `get_current_user` internally so only one `Depends`
    is needed per route parameter.

    Parameters
    ----------
    minimum_role : RoleEnum
        The minimum role required to access the route.
        Users with this role OR a more privileged role are allowed.

    Returns
    -------
    Callable
        An async FastAPI dependency that either returns the authenticated
        User or raises HTTP 403.

    Raises
    ------
    HTTPException(403)
        If the authenticated user's role is below `minimum_role` in the
        RBAC hierarchy.

    Usage
    -----
        # Only RESPONSABLE_IT and ADMINISTRATEUR can delete articles
        @router.delete("/{id}")
        async def delete(
            id: int,
            _: User = Depends(require_role(RoleEnum.RESPONSABLE_IT)),
        ):
            ...

        # Only ADMINISTRATEUR can access user management
        @router.get("/users")
        async def list_users(
            _: User = Depends(require_role(RoleEnum.ADMINISTRATEUR)),
        ):
            ...
    """
    async def _check_role(current_user=Depends(get_current_user)):
        try:
            user_level = _ROLE_HIERARCHY.index(RoleEnum(current_user.role))
            required_level = _ROLE_HIERARCHY.index(minimum_role)
        except ValueError:
            # Unknown role value — deny access conservatively.
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied — unrecognised role.",
            )

        if user_level < required_level:
            logger.warning(
                "Access denied: user id=%s role=%s tried to access resource "
                "requiring minimum role=%s.",
                current_user.id,
                current_user.role,
                minimum_role.value,
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"Permission denied. "
                    f"Required role: {minimum_role.value}. "
                    f"Your role: {current_user.role}."
                ),
            )

        return current_user

    return _check_role
