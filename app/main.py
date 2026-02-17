"""
TaskForge - A FastAPI-based task and project management application.

This module initializes the FastAPI application, registers all routers,
and creates the database tables.
"""
from fastapi import FastAPI

import app.database as db
from app.routers.auth import auth_router
from app.routers.projects import project_router
from app.routers.tasks import task_router, task_detail_router

TaskForge = FastAPI()

TaskForge.include_router(auth_router)
TaskForge.include_router(project_router)
TaskForge.include_router(task_router)
TaskForge.include_router(task_detail_router)

db.Base.metadata.create_all(bind=db.engine)


@TaskForge.get("/")
async def root():
    """
    Root endpoint that returns a welcome message.

    Returns:
        dict: A simple greeting message
    """
    return {"message": "Welcome to TaskForge! Go to the /docs page to try out the app."}


@TaskForge.get("/health")
async def health():
    """
    Health check endpoint to verify the API is running.

    Returns:
        dict: Status indicator showing the service is operational
    """
    return {"status": "ok"}
