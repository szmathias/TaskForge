"""
FastAPI dependency functions for request handling.

This module provides dependency functions used across API endpoints,
particularly for user authentication and authorization.
"""
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.auth import verify_access_token
from app.database import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Retrieve the current authenticated user from the JWT token.

    Args:
        token: JWT access token from the Authorization header
        db: Database session dependency

    Returns:
        User: The authenticated user object

    Raises:
        HTTPException: If token is invalid or user not found
    """
    email: str = verify_access_token(token)
    user: User | None = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
