
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.testing import exclude

from app import model
from app.schemas import product_schema
from app.database import get_db
from typing import List

router = APIRouter(prefix="/Product", tags=["product"])

@router.post("/create_product", response_model= product_schema.ProductResponse)
async def create_product(product: product_schema.ProductCreate, db: Session = Depends(get_db)):
    new_product= model.Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/Get_all_Product", response_model=List[product_schema.ProductResponse])
async def read_products(db: Session = Depends(get_db)):
    products = db.query(model.Product).all()
    return products


@router.get("/Get_Product/{product_id}", response_model=product_schema.ProductResponse)
async def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(model.Product).filter(model.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/Update_Product/{product_id}", response_model=product_schema.ProductResponse)
async def update_product(product_id: int, data: product_schema.ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(model.Product).filter(model.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(product, key, value)  # update value

    db.commit()
    db.refresh(product)
    return product

@router.delete("/Delete_Product/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(model.Product).filter(model.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return{"message":"Product deleted successfully"}