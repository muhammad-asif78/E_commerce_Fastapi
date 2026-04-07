from typing import Literal

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    account_type: Literal["user", "admin"] = "user"


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    account_type: Literal["user", "admin"]
    display_name: str | None = None


class AuthenticatedAccount(BaseModel):
    id: int
    username: str
    email: EmailStr
    account_type: Literal["user", "admin"]
    name: str | None = None
    is_superadmin: bool | None = None
