"""
User-related Pydantic schemas for request/response validation.

This module defines schemas for user registration, authentication,
and API responses.
"""
from datetime import datetime

from pydantic import BaseModel


class UserCreate(BaseModel):
    """
    Schema for user registration request.

    Attributes:
        email: User's email address
        password: Plain text password (will be hashed)
    """
    email: str
    password: str


class UserResponse(BaseModel):
    """
    Schema for user data in API responses.

    Attributes:
        id: User's unique identifier
        email: User's email address
        created_at: Account creation timestamp
    """
    id: int
    email: str
    created_at: datetime


class Token(BaseModel):
    """
    Schema for JWT token response.

    Attributes:
        access_token: JWT access token string
        token_type: Token type (always "bearer")
    """
    access_token: str
    token_type: str
