from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import get_env


db_url = get_env("DATABASE_URL")
if not db_url:
    raise RuntimeError(
        "DATABASE_URL is not set. Add it to the project root .env file "
        "or app/.env before starting the server."
    )

engine_kwargs = {"echo": True}
if db_url.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(db_url, **engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
