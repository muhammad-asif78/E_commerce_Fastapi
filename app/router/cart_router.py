from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.schemas import cart_schema
from app import model

from app.database import get_db

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/", response_model=cart_schema.CartResponse)
def create_cart(cart: cart_schema.CartCreate, db: Session = Depends(get_db)):
    new_cart = model.Cart(
        user_id=cart.user_id,
        product_id=cart.product_id,
        order_id=cart.order_id,
        created_at=str(datetime.now()),
        updated_at=str(datetime.now())
    )
    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)
    return new_cart


@router.get("/", response_model=list[cart_schema.CartResponse])
def get_all_carts(db: Session = Depends(get_db)):
    return db.query(model.Cart).all()


@router.get("/{cart_id}", response_model=cart_schema.CartResponse)
def get_cart(cart_id: int, db: Session = Depends(get_db)):
    cart = db.query(model.Cart).filter(model.Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart


@router.delete("/{cart_id}")
def delete_cart(cart_id: int, db: Session = Depends(get_db)):
    cart = db.query(model.Cart).filter(model.Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    db.delete(cart)
    db.commit()
    return {"message": "Cart deleted successfully"}
