from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class AdminCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_superadmin: Optional[bool] = False

class AdminUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_superadmin: Optional[bool] = None

class AdminResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_superadmin: bool
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True
