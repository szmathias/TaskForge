from fastapi import FastAPI
import app.database as db

TaskForge = FastAPI()

db.Base.metadata.create_all(bind=db.engine)

@TaskForge.get("/")
async def root():
    return {"message": "Hello, test!"}

@TaskForge.get("/health")
async def health():
    return {"status": "ok"}