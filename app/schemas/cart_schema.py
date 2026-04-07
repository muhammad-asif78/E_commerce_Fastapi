from pydantic import BaseModel
from datetime import datetime


class CartBase(BaseModel):
    user_id: int
    product_id: int
    order_id: int


class CartCreate(CartBase):
    pass


class CartUpdate(CartBase):
    created_at: datetime
    updated_at: datetime


class CartResponse(CartBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # ✅ replaces orm_mode in Pydantic v2
