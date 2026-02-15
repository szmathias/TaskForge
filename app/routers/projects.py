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


# Create a project, setting the owner_id to the current user's ID
@project_router.post("/", response_model=ProjectResponse)
def create_project(project_create: ProjectCreate, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)) -> ProjectResponse:
    new_project = Project(title=project_create.title, description=project_create.description, owner_id=current_user.id)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return ProjectResponse(id=new_project.id, title=new_project.title, description=new_project.description,
                           owner_id=new_project.owner_id, created_at=new_project.created_at)


# List only the current user's projects
@project_router.get("/", response_model=list[ProjectResponse])
def list_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[
    ProjectResponse]:
    projects = db.query(Project).filter(Project.owner_id == current_user.id).all()
    return [
        ProjectResponse(id=project.id, title=project.title, description=project.description, owner_id=project.owner_id,
                        created_at=project.created_at) for project in projects]


# Get one project by ID, ensuring it belongs to the current user
@project_router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)) -> ProjectResponse:
    project = db.query(Project).filter(Project.id == project_id, Project.owner_id == current_user.id).first()
    if project is None:
        raise HTTPException(status_code=403, detail="Project not found or access denied")
    return ProjectResponse(id=project.id, title=project.title, description=project.description,
                           owner_id=project.owner_id, created_at=project.created_at)


# Update a project, ensuring it belongs to the current user
@project_router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project_update: ProjectUpdate, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)) -> ProjectResponse:
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


# Delete a project, ensuring it belongs to the current user
@project_router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)) -> dict:
    project = db.query(Project).filter(Project.id == project_id, Project.owner_id == current_user.id).first()
    if project is None:
        raise HTTPException(status_code=403, detail="Project not found or access denied")

    db.delete(project)
    db.commit()
    return {"detail": "Project deleted successfully"}
