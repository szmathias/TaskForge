"""
Task database model.

This module defines the Task SQLAlchemy model representing
individual tasks within projects with status tracking and assignment.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Task(Base):
    """
    Task model representing a work item within a project.

    Attributes:
        id: Unique identifier for the task
        name: Task name
        description: Task description
        status: Current status (todo, in_progress, done)
        priority: Task priority level (low, medium, high)
        due_date: Optional deadline for task completion
        project_id: Foreign key to the parent project
        assignee_id: Foreign key to assigned user (optional)
        created_at: Timestamp of task creation
        updated_at: Timestamp of last update
        project: Relationship to the parent project
        assignee: Relationship to the assigned user
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, default="todo", nullable=False)
    priority = Column(String, default="medium", nullable=False)
    due_date = Column(DateTime, nullable=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    assignee_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User")
