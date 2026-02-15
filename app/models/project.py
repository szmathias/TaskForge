"""
Project database model.

This module defines the Project SQLAlchemy model representing
projects that contain tasks and are owned by users.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Project(Base):
    """
    Project model representing a collection of tasks.

    Attributes:
        id: Unique identifier for the project
        title: Project title
        description: Project description
        owner_id: Foreign key to the user who owns this project
        created_at: Timestamp of project creation
        owner: Relationship to the owning user
        tasks: Relationship to project's tasks (cascade delete)
    """
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    owner = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
