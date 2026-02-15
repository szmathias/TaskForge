"""
Task-related Pydantic schemas for request/response validation.

This module defines schemas for task creation, updates, API responses,
and enumerations for task status and priority.
"""
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class TaskStatus(str, Enum):
    """
    Enumeration of possible task status values.

    Values:
        TODO: Task not yet started
        IN_PROGRESS: Task currently being worked on
        DONE: Task completed
    """
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskPriority(str, Enum):
    """
    Enumeration of task priority levels.

    Values:
        LOW: Low priority task
        MEDIUM: Medium priority task
        HIGH: High priority task
    """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskCreate(BaseModel):
    """
    Schema for task creation request.

    Attributes:
        name: Task name
        description: Optional task description
        priority: Optional task priority (defaults to medium)
        due_date: Optional deadline
        assignee_id: Optional ID of user to assign task to
    """
    name: str
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    assignee_id: Optional[int] = None


class TaskResponse(BaseModel):
    """
    Schema for task data in API responses.

    Attributes:
        id: Task's unique identifier
        name: Task name
        description: Task description
        status: Current task status
        priority: Task priority level
        due_date: Task deadline
        assignee_id: ID of assigned user
        project_id: ID of parent project
        created_at: Task creation timestamp
        updated_at: Last update timestamp
    """
    id: int
    name: str
    description: Optional[str] = None
    status: TaskStatus
    priority: TaskPriority
    due_date: Optional[datetime] = None
    assignee_id: Optional[int] = None
    project_id: int
    created_at: datetime
    updated_at: datetime


class TaskUpdate(BaseModel):
    """
    Schema for task update request.

    All fields are optional to allow partial updates.

    Attributes:
        name: Updated task name
        description: Updated task description
        status: Updated task status
        priority: Updated task priority
        due_date: Updated deadline
        assignee_id: Updated assignee
    """
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    assignee_id: Optional[int] = None
