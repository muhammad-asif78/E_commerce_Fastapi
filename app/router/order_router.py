from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import order_schema
from app import model
from app.schemas import order_schema
from app.database import get_db


router = APIRouter(prefix="/order", tags=["orders"])

@router.post("/create_order", response_model= order_schema.OrderResponse)
async def create_order(order: order_schema.OrderCreate, db: Session = Depends(get_db)):
    new_order = model.Order(**order.dict())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order


@router.get("/get_all_orders", response_model=List[order_schema.OrderResponse])
async def get_all_orders(db: Session = Depends(get_db)):
    orders = db.query(model.Order).all()
    return orders

@router.get("/get_order/{order_id}", response_model=order_schema.OrderResponse)
async def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(model.Order).filter(model.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/update_order/{order_id}", response_model=order_schema.OrderResponse)
async def update_order(order_id: int, data: order_schema.OrderUpdate, db: Session = Depends(get_db)):
    order = db.query(model.Order).filter(model.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(order, key, value)

    db.commit()
    db.refresh(order)
    return order

@router.delete("/delete_order/{order_id}")
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(model.Order).filter(model.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}
