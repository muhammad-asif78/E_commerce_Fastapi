from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import model
from app.auth import get_current_admin, get_current_principal, get_current_user, hash_password
from app.schemas import user_schma as schemas


from app.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


def _ensure_user_access(user_id: int, principal: dict) -> None:
    if principal["account_type"] == "admin":
        return

    current_user = principal["account"]
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own user record",
        )


# Create User
@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(model.User).filter(model.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = model.User(
        username=user.username,
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Get All Users
@router.get("/", response_model=list[schemas.UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_admin: model.Admin = Depends(get_current_admin),
):
    return db.query(model.User).all()


@router.get("/me", response_model=schemas.UserResponse)
def get_me(current_user: model.User = Depends(get_current_user)):
    return current_user


# Get User by ID
@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    principal: dict = Depends(get_current_principal),
):
    _ensure_user_access(user_id, principal)
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Update User
@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(
    user_id: int,
    user_data: schemas.UserUpdate,
    db: Session = Depends(get_db),
    principal: dict = Depends(get_current_principal),
):
    _ensure_user_access(user_id, principal)
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.username = user_data.username
    user.name = user_data.name
    user.email = user_data.email
    if user_data.password:
        user.password = hash_password(user_data.password)

    db.commit()
    db.refresh(user)
    return user


# Delete User
@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    principal: dict = Depends(get_current_principal),
):
    _ensure_user_access(user_id, principal)
    user = db.query(model.User).filter(model.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": f"User with ID {user_id} deleted successfully"}

