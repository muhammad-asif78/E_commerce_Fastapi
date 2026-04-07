import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_CANDIDATES = (
    BASE_DIR / ".env",
    BASE_DIR / "app" / ".env",
)


def load_environment() -> None:
    for env_path in ENV_CANDIDATES:
        if env_path.exists():
            load_dotenv(env_path, override=False)


def get_env(name: str, default: str | None = None) -> str | None:
    load_environment()
    return os.getenv(name, default)


load_environment()
