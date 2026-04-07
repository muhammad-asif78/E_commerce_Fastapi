from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    name: str | None = None
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: str | None = None


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

