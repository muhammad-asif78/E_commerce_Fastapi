from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from app.auth import (
    get_current_admin,
    get_current_admin_optional,
    get_current_superadmin,
    hash_password,
)
from app.schemas import admin_schema
from app import model
from app.database import get_db

router = APIRouter(prefix="/admins", tags=["Admin"])


@router.post("/create_admin", response_model=admin_schema.AdminResponse)
def create_admin(
    admin: admin_schema.AdminCreate,
    db: Session = Depends(get_db),
    current_admin: model.Admin | None = Depends(get_current_admin_optional),
):
    if db.query(model.Admin).count() > 0:
        if current_admin is None or not current_admin.is_superadmin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only a superadmin can create additional admins",
            )

    # Check if admin already exists (by email or username)
    existing_admin = db.query(model.Admin).filter(
        (model.Admin.email == admin.email) | (model.Admin.username == admin.username)
    ).first()
    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin with this email or username already exists",
        )

    current_time = datetime.utcnow()

    new_admin = model.Admin(
        username=admin.username,
        email=admin.email,
        password=hash_password(admin.password),
        is_superadmin=admin.is_superadmin,
        created_at=str(current_time),
        updated_at=str(current_time),
    )

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin


@router.get("/get_all_admins", response_model=List[admin_schema.AdminResponse])
def get_all_admins(
    db: Session = Depends(get_db),
    current_admin: model.Admin = Depends(get_current_admin),
):
    admins = db.query(model.Admin).all()
    return admins


@router.get("/me", response_model=admin_schema.AdminResponse)
def get_me(current_admin: model.Admin = Depends(get_current_admin)):
    return current_admin


@router.get("/get_admin/{admin_id}", response_model=admin_schema.AdminResponse)
def get_admin(
    admin_id: int,
    db: Session = Depends(get_db),
    current_admin: model.Admin = Depends(get_current_admin),
):
    admin = db.query(model.Admin).filter(model.Admin.id == admin_id).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found",
        )
    return admin

@router.put("/update_admin/{admin_id}", response_model=admin_schema.AdminResponse)
def update_admin(
    admin_id: int,
    admin_update: admin_schema.AdminUpdate,
    db: Session = Depends(get_db),
    current_admin: model.Admin = Depends(get_current_superadmin),
):
    admin = db.query(model.Admin).filter(model.Admin.id == admin_id).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found",
        )

    if admin_update.username is not None:
        admin.username = admin_update.username
    if admin_update.email is not None:
        admin.email = admin_update.email
    if admin_update.password is not None:
        admin.password = hash_password(admin_update.password)
    if admin_update.is_superadmin is not None:
        admin.is_superadmin = admin_update.is_superadmin

    admin.updated_at = str(datetime.utcnow())

    db.commit()
    db.refresh(admin)
    return admin


@router.delete("/delete_admin/{admin_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin(
    admin_id: int,
    db: Session = Depends(get_db),
    current_admin: model.Admin = Depends(get_current_superadmin),
):
    admin = db.query(model.Admin).filter(model.Admin.id == admin_id).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found",
        )

    db.delete(admin)
    db.commit()
    return None
