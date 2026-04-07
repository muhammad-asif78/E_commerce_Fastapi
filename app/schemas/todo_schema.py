from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class TodoBase(BaseModel):
    title: str
    description: str
    due_date: datetime

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None

class TodoResponse(TodoBase):
    id: int

    class Config:
        orm_mode = True
