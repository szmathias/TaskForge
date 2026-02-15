from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class ProjectCreate(BaseModel):
    title: str
    description: str

class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str
    owner_id: int
    created_at: datetime

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None