from curses.textpad import Textbox

from sqlalchemy import Column, Integer, String , ForeignKey, func, DateTime, Text, Boolean
from app.database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    name = Column(String(100))
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(String(100), nullable=False)
    image = Column(String(100), nullable=False)
    stock = Column(String(100), nullable=False)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    items = Column(String(100), nullable=False)
    total_amount = Column(String(100), nullable=False)
    status = Column(String(100), nullable=False)
    shipping_address = Column(String(100), nullable=False)

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    created_at = Column(String(100), nullable=False)
    updated_at = Column(String(100), nullable=False)

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    due_date = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

class  Email(Base):
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(Text, nullable=False)


class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    is_superadmin = Column(Boolean, default=False)
    created_at = Column(String(100), default=str(datetime.utcnow()))
    updated_at = Column(String(100), default=str(datetime.utcnow()))