"""
Authentication utilities for password hashing and JWT token management.

This module provides functions for secure password handling using bcrypt
and JWT token creation/verification for user authentication.
"""
from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    Hash a plain text password using bcrypt.

    Args:
        password: The plain text password to hash

    Returns:
        str: The hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.

    Args:
        plain_password: The plain text password to verify
        hashed_password: The hashed password to compare against

    Returns:
        bool: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """
    Create a JWT access token with expiration time.

    Args:
        data: Dictionary containing claims to encode in the token

    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    expires_in = datetime.utcnow() + timedelta(minutes=settings.access_token_expiration_minutes)
    to_encode.update({"exp": expires_in})
    return jwt.encode(to_encode, settings.secret_key, algorithm="HS256")


def verify_access_token(token: str) -> str:
    """
    Verify and decode a JWT access token to extract the user email.

    Args:
        token: The JWT token to verify

    Returns:
        str: The email address extracted from the token

    Raises:
        HTTPException: If token is invalid or missing email claim
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
