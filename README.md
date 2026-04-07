# E-Commerce FastAPI

Backend API for an e-commerce project built with FastAPI, SQLAlchemy, bearer-token authentication, and Alembic migrations.

## Features

- FastAPI REST API with interactive Swagger docs at `/docs`
- Bearer token authentication for users and admins
- Admin and user account management
- Product, order, cart, todo, and email CRUD endpoints
- SQLAlchemy ORM models
- Alembic migration setup included in the repository
- Environment-based configuration with `.env`

## Tech Stack

- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- Passlib
- PostgreSQL

## Project Structure

```text
.
├── alembic/
│   ├── env.py
│   └── versions/
├── app/
│   ├── auth.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── model.py
│   ├── router/
│   └── schemas/
├── alembic.ini
├── pyproject.toml
└── README.md
```

## Environment Variables

Create a local `.env` file in the project root. A safe template is provided in `.env.example`.

Required values:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/e_commerce
SECRET_KEY=replace-with-a-long-random-secret
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
```

If you use `uv`, you can also install from the lockfile:

```bash
uv sync
```

## Run The App

```bash
.venv/bin/python -m uvicorn app.main:app --reload
```

Open:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Authentication

1. Create an admin with `POST /admins/create_admin`
2. Login with `POST /auth/login`
3. Copy the `access_token`
4. In Swagger, click `Authorize` and paste only the token

## Database Migrations

Alembic configuration and migration files are already included.

Run migrations:

```bash
alembic upgrade head
```

Create a new migration:

```bash
alembic revision --autogenerate -m "your_message"
```

## Main API Areas

- Authentication
- Admin
- Users
- Product
- Orders
- Cart
- Todos
- Email

## Notes

- Real `.env` files are intentionally ignored by Git for security.
- Alembic files are included and ready to version with the project.
- Swagger authorization is configured for token-only bearer input.

## License

This project is available for personal and educational use unless you define a different license for deployment or distribution.
