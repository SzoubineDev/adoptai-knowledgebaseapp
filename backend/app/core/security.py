"""
Auth Étape 3 - Core Security Utilities
Project : AdoptAI App Knowledge Base
Author  : Oussama
Feature : Auth (Sécurité & Authentification)

This module centralises all cryptographic operations for the authentication
system. It is intentionally kept pure (no FastAPI, no Prisma) so it can be
unit-tested without any infrastructure dependency.

Responsibilities
----------------
1. Password hashing and verification  — via passlib / bcrypt
2. JWT access-token creation          — via python-jose
3. JWT token decoding / verification  — used by app/dependencies/auth.py

Why a dedicated module?
-----------------------
Keeping security primitives in one place means:
  - A single audit surface for cryptographic code.
  - Route handlers and dependencies never call bcrypt or jose directly —
    they call these well-named helpers, improving readability.
  - All algorithm/scheme choices (bcrypt, HS256) are changed in one place.

Configuration (from app/core/config.py via settings)
------------------------------------------------------
  SECRET_KEY                 : HS256 signing secret — override in production!
                               Generate with: openssl rand -hex 32
  ALGORITHM                  : JWT algorithm ("HS256" by default)
  ACCESS_TOKEN_EXPIRE_MINUTES: Default token lifetime (30 min)

Usage
-----
  from app.core.security import (
      get_password_hash, verify_password,
      create_access_token, decode_access_token,
  )
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Password hashing context
# ---------------------------------------------------------------------------
# `schemes=["bcrypt"]`  — use only bcrypt (no legacy MD5/SHA1 fallback).
# `deprecated="auto"`   — automatically re-hash passwords stored with older
#                         schemes if we ever add new ones in the future.
# ---------------------------------------------------------------------------
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    Hash a plain-text password using bcrypt.

    The resulting hash includes the algorithm identifier, cost factor, and
    salt — all embedded in a single string that is safe to store in the DB.

    Parameters
    ----------
    password : str
        The plain-text password to hash. Must never be stored or logged.

    Returns
    -------
    str
        A bcrypt hash string, e.g.:
        ``$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW``

    Usage
    -----
        hashed = get_password_hash("my_plain_password")
        user = await db.user.create(data={"hashed_password": hashed, ...})
    """
    return _pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against a stored bcrypt hash.

    Uses constant-time comparison internally to prevent timing attacks.

    Parameters
    ----------
    plain_password   : str — the password submitted by the user at login.
    hashed_password  : str — the bcrypt hash retrieved from the database.

    Returns
    -------
    bool
        True  if the password matches the hash.
        False otherwise (never raises on mismatch — always returns bool).

    Usage
    -----
        if not verify_password(body.password, db_user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect password")
    """
    return _pwd_context.verify(plain_password, hashed_password)


# ---------------------------------------------------------------------------
# JWT helpers
# ---------------------------------------------------------------------------

def create_access_token(
    data: dict[str, Any],
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Create and sign a JWT access token.

    The token payload (`data`) is shallow-copied before modification to avoid
    mutating the caller's dict. The `exp` (expiration) claim is added
    automatically using UTC time.

    Parameters
    ----------
    data : dict
        Arbitrary claims to embed in the token payload.
        Convention: include ``"sub"`` (subject = user id as str) and
        ``"role"`` (user's RoleEnum value) so `get_current_user` can
        extract them without a DB round-trip for simple RBAC checks.

        Example:
            {"sub": str(user.id), "role": user.role}

    expires_delta : Optional[timedelta]
        Custom token lifetime. Defaults to ``ACCESS_TOKEN_EXPIRE_MINUTES``
        from settings (30 min) if not supplied.

    Returns
    -------
    str
        A signed JWT string in the form ``header.payload.signature``.

    Usage in route handler
    ----------------------
        from datetime import timedelta
        from app.core.security import create_access_token
        from app.core.config import settings

        token = create_access_token(
            data={"sub": str(user.id), "role": user.role},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        return Token(access_token=token, token_type="bearer")
    """
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta is not None
        else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode["exp"] = expire

    encoded_jwt: str = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    logger.debug(
        "JWT created — sub=%s exp=%s",
        to_encode.get("sub"),
        expire.isoformat(),
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Decode and verify a JWT access token.

    Validates:
      - Signature (using SECRET_KEY + ALGORITHM)
      - Expiration (`exp` claim) — raises JWTError if token is expired

    Parameters
    ----------
    token : str
        The raw JWT string from the ``Authorization: Bearer <token>`` header.

    Returns
    -------
    dict
        The decoded payload as a Python dict (e.g., ``{"sub": "1", "role": "RESPONSABLE_IT", "exp": ...}``).

    Raises
    ------
    jose.JWTError
        If the token is malformed, the signature is invalid, or the token
        has expired. The caller (`get_current_user`) converts this to an
        HTTP 401 response.

    Usage
    -----
        from app.core.security import decode_access_token
        from jose import JWTError

        try:
            payload = decode_access_token(token)
        except JWTError:
            raise credentials_exception
    """
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )
