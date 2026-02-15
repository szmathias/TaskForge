from fastapi import FastAPI
import app.database as db
from app.routers.auth import auth_router

TaskForge = FastAPI()
TaskForge.include_router(auth_router)

db.Base.metadata.create_all(bind=db.engine)

@TaskForge.get("/")
async def root():
    return {"message": "Hello, test!"}

@TaskForge.get("/health")
async def health():
    return {"status": "ok"}