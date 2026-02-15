"""
Project management router for CRUD operations.

This module provides endpoints for creating, reading, updating, and deleting
projects. All operations are scoped to the authenticated user.
"""
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectResponse, ProjectCreate, ProjectUpdate

project_router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@project_router.post("/", response_model=ProjectResponse)
def create_project(project_create: ProjectCreate, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)) -> ProjectResponse:
    """
    Create a new project for the authenticated user.

    Args:
        project_create: Project creation data with title and description
        db: Database session dependency
        current_user: Authenticated user dependency

    Returns:
        ProjectResponse: The created project information
    """
    new_project = Project(title=project_create.title, description=project_create.description, owner_id=current_user.id)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return ProjectResponse(id=new_project.id, title=new_project.title, description=new_project.description,
                           owner_id=new_project.owner_id, created_at=new_project.created_at)


@project_router.get("/", response_model=list[ProjectResponse])
def list_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[
    ProjectResponse]:
    """
    List all projects owned by the authenticated user.

    Args:
        db: Database session dependency
        current_user: Authenticated user dependency

    Returns:
        list[ProjectResponse]: List of projects owned by the user
    """
    projects = db.query(Project).filter(Project.owner_id == current_user.id).all()
    return [
        ProjectResponse(id=project.id, title=project.title, description=project.description, owner_id=project.owner_id,
                        created_at=project.created_at) for project in projects]


@project_router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)) -> ProjectResponse:
    """
    Get a specific project by ID if owned by the authenticated user.

    Args:
        project_id: The ID of the project to retrieve
        db: Database session dependency
        current_user: Authenticated user dependency

    Returns:
        ProjectResponse: The requested project information

    Raises:
        HTTPException: If project not found or user doesn't have access
    """
    project = db.query(Project).filter(Project.id == project_id, Project.owner_id == current_user.id).first()
    if project is None:
        raise HTTPException(status_code=403, detail="Project not found or access denied")
    return ProjectResponse(id=project.id, title=project.title, description=project.description,
                           owner_id=project.owner_id, created_at=project.created_at)


@project_router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project_update: ProjectUpdate, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)) -> ProjectResponse:
    """
    Update a project's title or description.

    Args:
        project_id: The ID of the project to update
        project_update: Updated project data
        db: Database session dependency
        current_user: Authenticated user dependency

    Returns:
        ProjectResponse: The updated project information

    Raises:
        HTTPException: If project not found or user doesn't have access
    """
    project = db.query(Project).filter(Project.id == project_id, Project.owner_id == current_user.id).first()
    if project is None:
        raise HTTPException(status_code=403, detail="Project not found or access denied")

    if project_update.title is not None:
        project.title = project_update.title
    if project_update.description is not None:
        project.description = project_update.description

    db.commit()
    db.refresh(project)
    return ProjectResponse(id=project.id, title=project.title, description=project.description,
                           owner_id=project.owner_id, created_at=project.created_at)


@project_router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)) -> dict:
    """
    Delete a project and all its associated tasks.

    Args:
        project_id: The ID of the project to delete
        db: Database session dependency
        current_user: Authenticated user dependency

    Returns:
        dict: Success message

    Raises:
        HTTPException: If project not found or user doesn't have access
    """
    project = db.query(Project).filter(Project.id == project_id, Project.owner_id == current_user.id).first()
    if project is None:
        raise HTTPException(status_code=403, detail="Project not found or access denied")

    db.delete(project)
    db.commit()
    return {"detail": "Project deleted successfully"}
