from typing import Optional

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.project import Project
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

task_router = APIRouter(
    prefix="/projects/{project_id}/tasks",
    tags=["Tasks"],
)

task_detail_router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


# create a task, ensuring the project belongs to the current user
@task_router.post("/", response_model=TaskResponse)
def create_task(project_id: int, task_create: TaskCreate, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)) -> TaskResponse:
    project = db.query(Project).filter(Project.id == project_id, Project.owner_id == current_user.id).first()
    if project is None:
        raise HTTPException(status_code=403, detail="Project not found or access denied")

    new_task = Task(name=task_create.name, description=task_create.description, due_date=task_create.due_date,
                    assignee_id=task_create.assignee_id, project_id=project_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return TaskResponse(id=new_task.id, name=new_task.name, description=new_task.description, status=new_task.status,
                        priority=new_task.priority, due_date=new_task.due_date, project_id=new_task.project_id,
                        assignee_id=new_task.assignee_id, created_at=new_task.created_at,
                        updated_at=new_task.updated_at)


# list tasks for a project, ensuring the project belongs to the current user
@task_router.get("/", response_model=list[TaskResponse])
def list_tasks(project_id: int, status: Optional[str] = None, priority: Optional[str] = None,
               db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[TaskResponse]:
    project = db.query(Project).filter(Project.id == project_id, Project.owner_id == current_user.id).first()
    if project is None:
        raise HTTPException(status_code=403, detail="Project not found or access denied")

    query = db.query(Task).filter(Task.project_id == project_id)
    if status is not None:
        query = query.filter(Task.status == status)
    if priority is not None:
        query = query.filter(Task.priority == priority)

    tasks = query.all()
    return [TaskResponse(id=task.id, name=task.name, description=task.description, status=task.status,
                         priority=task.priority, due_date=task.due_date, project_id=task.project_id,
                         assignee_id=task.assignee_id, created_at=task.created_at, updated_at=task.updated_at) for task
            in tasks]


# get a task by ID, ensuring the project belongs to the current user
@task_detail_router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db),
             current_user: User = Depends(get_current_user)) -> TaskResponse:
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    project = db.query(Project).filter(Project.id == task.project_id, Project.owner_id == current_user.id).first()
    if project is None:
        raise HTTPException(status_code=403, detail="Access denied")

    return TaskResponse(id=task.id, name=task.name, description=task.description, status=task.status,
                        priority=task.priority, due_date=task.due_date, project_id=task.project_id,
                        assignee_id=task.assignee_id, created_at=task.created_at, updated_at=task.updated_at)


# update a task, ensuring the project belongs to the current user
@task_detail_router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)) -> TaskResponse:
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    project = db.query(Project).filter(Project.id == task.project_id, Project.owner_id == current_user.id).first()
    if project is None:
        raise HTTPException(status_code=403, detail="Access denied")

    if task_update.name is not None:
        task.name = task_update.name
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.status is not None:
        task.status = task_update.status
    if task_update.priority is not None:
        task.priority = task_update.priority
    if task_update.due_date is not None:
        task.due_date = task_update.due_date
    if task_update.assignee_id is not None:
        task.assignee_id = task_update.assignee_id

    db.commit()
    db.refresh(task)
    return TaskResponse(id=task.id, name=task.name, description=task.description, status=task.status,
                        priority=task.priority, due_date=task.due_date, project_id=task.project_id,
                        assignee_id=task.assignee_id, created_at=task.created_at, updated_at=task.updated_at)


# delete a task, ensuring the project belongs to the current user
@task_detail_router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> dict:
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    project = db.query(Project).filter(Project.id == task.project_id, Project.owner_id == current_user.id).first()
    if project is None:
        raise HTTPException(status_code=403, detail="Access denied")

    db.delete(task)
    db.commit()
    return {"detail": "Task deleted successfully"}
