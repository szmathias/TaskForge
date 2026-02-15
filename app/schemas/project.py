"""
Project-related Pydantic schemas for request/response validation.

This module defines schemas for project creation, updates,
and API responses.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProjectCreate(BaseModel):
    """
    Schema for project creation request.

    Attributes:
        title: Project title
        description: Project description
    """
    title: str
    description: str


class ProjectResponse(BaseModel):
    """
    Schema for project data in API responses.

    Attributes:
        id: Project's unique identifier
        title: Project title
        description: Project description
        owner_id: ID of the user who owns this project
        created_at: Project creation timestamp
    """
    id: int
    title: str
    description: str
    owner_id: int
    created_at: datetime


class ProjectUpdate(BaseModel):
    """
    Schema for project update request.

    All fields are optional to allow partial updates.

    Attributes:
        title: Updated project title
        description: Updated project description
    """
    title: Optional[str] = None
    description: Optional[str] = None
