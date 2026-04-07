import base64
import hashlib
import hmac
import json
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app import model
from app.config import get_env
from app.database import get_db


pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
bearer_scheme = HTTPBearer(
    bearerFormat="JWT",
    description="Paste only the access token here.",
)
optional_bearer_scheme = HTTPBearer(
    bearerFormat="JWT",
    description="Paste only the access token here.",
    auto_error=False,
)

SECRET_KEY = get_env("SECRET_KEY", "change-this-secret-key")
ACCESS_TOKEN_EXPIRE_MINUTES = int(get_env("ACCESS_TOKEN_EXPIRE_MINUTES", "60") or "60")
ALGORITHM = "HS256"

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, stored_password: str) -> bool:
    if not stored_password:
        return False

    try:
        if stored_password.startswith("$"):
            return pwd_context.verify(plain_password, stored_password)
    except Exception:
        return False

    return secrets.compare_digest(plain_password, stored_password)


def authenticate_user(db: Session, email: str, password: str) -> model.User | None:
    user = db.query(model.User).filter(model.User.email == email).first()
    if user and verify_password(password, user.password):
        return user
    return None


def authenticate_admin(db: Session, email: str, password: str) -> model.Admin | None:
    admin = db.query(model.Admin).filter(model.Admin.email == email).first()
    if admin and verify_password(password, admin.password):
        return admin
    return None


def _base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


def _base64url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


def _json_bytes(data: dict[str, Any]) -> bytes:
    return json.dumps(data, separators=(",", ":"), sort_keys=True).encode("utf-8")


def create_access_token(subject_id: int, account_type: str, expires_delta: timedelta | None = None) -> str:
    expires_at = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    header = {"alg": ALGORITHM, "typ": "JWT"}
    payload = {
        "sub": str(subject_id),
        "account_type": account_type,
        "exp": int(expires_at.timestamp()),
    }

    encoded_header = _base64url_encode(_json_bytes(header))
    encoded_payload = _base64url_encode(_json_bytes(payload))
    signing_input = f"{encoded_header}.{encoded_payload}".encode("utf-8")
    signature = hmac.new(
        SECRET_KEY.encode("utf-8"),
        signing_input,
        hashlib.sha256,
    ).digest()
    encoded_signature = _base64url_encode(signature)
    return f"{encoded_header}.{encoded_payload}.{encoded_signature}"


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        encoded_header, encoded_payload, encoded_signature = token.split(".")
    except ValueError as exc:
        raise CREDENTIALS_EXCEPTION from exc

    signing_input = f"{encoded_header}.{encoded_payload}".encode("utf-8")
    expected_signature = hmac.new(
        SECRET_KEY.encode("utf-8"),
        signing_input,
        hashlib.sha256,
    ).digest()

    try:
        provided_signature = _base64url_decode(encoded_signature)
        header = json.loads(_base64url_decode(encoded_header))
        payload = json.loads(_base64url_decode(encoded_payload))
    except (ValueError, json.JSONDecodeError) as exc:
        raise CREDENTIALS_EXCEPTION from exc

    if header.get("alg") != ALGORITHM:
        raise CREDENTIALS_EXCEPTION

    if not hmac.compare_digest(provided_signature, expected_signature):
        raise CREDENTIALS_EXCEPTION

    expires_at = payload.get("exp")
    if not isinstance(expires_at, int):
        raise CREDENTIALS_EXCEPTION

    if datetime.now(timezone.utc).timestamp() >= expires_at:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


def _load_account(db: Session, account_type: str, subject_id: str) -> model.User | model.Admin | None:
    try:
        account_id = int(subject_id)
    except (TypeError, ValueError):
        return None

    if account_type == "user":
        return db.query(model.User).filter(model.User.id == account_id).first()
    if account_type == "admin":
        return db.query(model.Admin).filter(model.Admin.id == account_id).first()
    return None


def get_current_principal(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> dict[str, Any]:
    token = credentials.credentials
    payload = decode_access_token(token)
    subject_id = payload.get("sub")
    account_type = payload.get("account_type")
    if not subject_id or account_type not in {"user", "admin"}:
        raise CREDENTIALS_EXCEPTION

    account = _load_account(db, account_type, subject_id)
    if account is None:
        raise CREDENTIALS_EXCEPTION

    return {"account_type": account_type, "account": account}


def get_current_user(
    principal: dict[str, Any] = Depends(get_current_principal),
) -> model.User:
    if principal["account_type"] != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User credentials are required for this endpoint",
        )
    return principal["account"]


def get_current_admin(
    principal: dict[str, Any] = Depends(get_current_principal),
) -> model.Admin:
    if principal["account_type"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin credentials are required for this endpoint",
        )
    return principal["account"]


def get_current_admin_optional(
    credentials: HTTPAuthorizationCredentials | None = Depends(optional_bearer_scheme),
    db: Session = Depends(get_db),
) -> model.Admin | None:
    if credentials is None:
        return None

    token = credentials.credentials
    payload = decode_access_token(token)
    subject_id = payload.get("sub")
    account_type = payload.get("account_type")
    if not subject_id or account_type != "admin":
        raise CREDENTIALS_EXCEPTION

    try:
        admin_id = int(subject_id)
    except (TypeError, ValueError) as exc:
        raise CREDENTIALS_EXCEPTION from exc

    admin = db.query(model.Admin).filter(model.Admin.id == admin_id).first()
    if admin is None:
        raise CREDENTIALS_EXCEPTION

    return admin


def get_current_superadmin(
    current_admin: model.Admin = Depends(get_current_admin),
) -> model.Admin:
    if not current_admin.is_superadmin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Superadmin access is required for this endpoint",
        )
    return current_admin
