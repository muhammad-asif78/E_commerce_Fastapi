from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import (
    authenticate_admin,
    authenticate_user,
    create_access_token,
    get_current_principal,
)
from app.database import get_db
from app.schemas import auth_schema


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=auth_schema.TokenResponse)
def login(credentials: auth_schema.LoginRequest, db: Session = Depends(get_db)):
    if credentials.account_type == "admin":
        account = authenticate_admin(db, credentials.email, credentials.password)
        display_name = account.username if account else None
    else:
        account = authenticate_user(db, credentials.email, credentials.password)
        display_name = account.username if account else None

    if account is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        subject_id=account.id,
        account_type=credentials.account_type,
    )
    return auth_schema.TokenResponse(
        access_token=access_token,
        token_type="bearer",
        account_type=credentials.account_type,
        display_name=display_name,
    )


@router.get("/me", response_model=auth_schema.AuthenticatedAccount)
def read_current_account(principal: dict = Depends(get_current_principal)):
    account = principal["account"]
    return auth_schema.AuthenticatedAccount(
        id=account.id,
        username=account.username,
        email=account.email,
        account_type=principal["account_type"],
        name=getattr(account, "name", None),
        is_superadmin=getattr(account, "is_superadmin", None),
    )
