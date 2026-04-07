from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
     name: str
     description: str
     price: int
     category: str
     image: str
     stock: int


class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    category: Optional[str] = None
    image: Optional[str] = None
    stock: Optional[int] = None

class ProductResponse(ProductBase):
    id: int
    class Config:
        orm_mode = True