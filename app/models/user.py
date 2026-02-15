"""
User database model.

This module defines the User SQLAlchemy model representing
application users with authentication credentials.
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    """
    User model representing authenticated users in the system.

    Attributes:
        id: Unique identifier for the user
        email: User's email address (unique)
        hashed_password: Bcrypt-hashed password
        created_at: Timestamp of user registration
        projects: Relationship to user's owned projects
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    projects = relationship("Project", back_populates="owner")
