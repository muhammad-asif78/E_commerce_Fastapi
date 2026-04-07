from fastapi import FastAPI
from app.database import Base, engine
from app.router import user_router , product_router, order_router, cart_router, todo_router, email_routers, admin_router, auth_router

# Create database tables
Base.metadata.create_all(bind=engine)

openapi_tags = [
    {"name": "Authentication"},
    {"name": "Admin"},
    {"name": "Users"},
    {"name": "product"},
    {"name": "orders"},
    {"name": "Cart"},
    {"name": "Todos"},
    {"name": "email"},
]

# This is the key object Uvicorn looks for
app = FastAPI(title="E-Commerce FastAPI", openapi_tags=openapi_tags)

# Include routers
app.include_router(user_router.router)
app.include_router(product_router.router)
app.include_router(order_router.router)
app.include_router(cart_router.router)
app.include_router(todo_router.router)
app.include_router(email_routers.router)
app.include_router(admin_router.router)
app.include_router(auth_router.router)


@app.get("/")
def home():
    return {"message": "Welcome to E-Commerce FastAPI!"}
