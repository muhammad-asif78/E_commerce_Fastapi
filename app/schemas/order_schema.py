from typing import Optional

from pydantic import BaseModel


class OrderBase(BaseModel):
    user_id: int
    items: int
    total_amount: int
    status: str
    shipping_address: str


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    user_id: Optional[int] = None
    items: Optional[int] = None
    total_amount: Optional[int] = None
    status: Optional[str] = None
    shipping_address: Optional[str] = None


class OrderResponse(OrderBase):
    id: int

    class Config:
        orm_mode = True





