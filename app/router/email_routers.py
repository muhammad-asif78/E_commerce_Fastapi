from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import model
from app.schemas import email_schema
from app.database import get_db

router = APIRouter(prefix="/email", tags=["email"])


@router.post("/", response_model=email_schema.EmailResponse)
def create_email(email: email_schema.EmailCreate, db: Session = Depends(get_db)):
    new_email = model.Email(email=email.email)
    db.add(new_email)
    db.commit()
    db.refresh(new_email)
    return new_email


@router.get("/", response_model=list[email_schema.EmailResponse])
def get_all_emails(db: Session = Depends(get_db)):
    emails = db.query(model.Email).all()
    return emails


@router.get("/{email_id}", response_model=email_schema.EmailResponse)
def get_email(email_id: int, db: Session = Depends(get_db)):
    email = db.query(model.Email).filter(model.Email.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    return email


@router.put("/{email_id}", response_model=email_schema.EmailResponse)
def update_email(email_id: int, updated_email: email_schema.EmailUpdate, db: Session = Depends(get_db)):
    email = db.query(model.Email).filter(model.Email.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")

    email.email = updated_email.email
    db.commit()
    db.refresh(email)
    return email


@router.delete("/{email_id}")
def delete_email(email_id: int, db: Session = Depends(get_db)):
    email = db.query(model.Email).filter(model.Email.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")

    db.delete(email)
    db.commit()
    return {"message": "Email deleted successfully"}
