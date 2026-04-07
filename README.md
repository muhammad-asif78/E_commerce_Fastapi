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
- Repository guidance in `CLAUDE.md`

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
├── CLAUDE.md
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
├── .env.example
├── pyproject.toml
└── README.md
```

## Main Modules

- `app/main.py` -> FastAPI app creation and router registration
- `app/auth.py` -> password hashing, token creation/validation, auth dependencies
- `app/config.py` -> environment variable loading
- `app/database.py` -> SQLAlchemy engine and session setup
- `app/model.py` -> database models
- `app/router/` -> API endpoints
- `app/schemas/` -> Pydantic request/response models
- `alembic/` -> migration configuration and revision history

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

## Quick Start

1. Create and activate the virtual environment
2. Copy `.env.example` to `.env`
3. Update `DATABASE_URL` and `SECRET_KEY`
4. Run database migrations
5. Start the API server

Example:

```bash
cp .env.example .env
alembic upgrade head
.venv/bin/python -m uvicorn app.main:app --reload
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

Example login payload:

```json
{
  "email": "admin@example.com",
  "password": "admin123",
  "account_type": "admin"
}
```

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

## Security Notes

- Real `.env` files are intentionally ignored by Git
- Keep `SECRET_KEY` private and unique per environment
- Use bearer tokens only over trusted HTTPS deployments
- Review `CLAUDE.md` before making auth, admin, or migration changes

## Git Workflow

Use these commands to save and upload your changes:

```bash
git status
git add .
git commit -m "Your commit message"
git push origin main
```

If you want to push only selected files:

```bash
git add README.md
git commit -m "Update README"
git push origin main
```

## Notes

- Alembic files are included and ready to version with the project
- Swagger authorization is configured for token-only bearer input
- Repository-specific engineering and security guidance lives in `CLAUDE.md`

## License

This project is available for personal and educational use unless you define a different license for deployment or distribution.
