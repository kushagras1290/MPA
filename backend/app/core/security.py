from datetime import UTC, datetime, timedelta
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return str(password_context.hash(password))


def verify_password(password: str, hashed_password: str) -> bool:
    return bool(password_context.verify(password, hashed_password))


def create_access_token(subject: str, claims: dict[str, Any] | None = None) -> str:
    if not settings.jwt_secret:
        raise ValueError("JWT_SECRET must be configured before issuing access tokens.")

    now = datetime.now(UTC)
    payload: dict[str, Any] = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=settings.access_token_expire_minutes)).timestamp()),
    }
    if claims:
        payload.update(claims)
    return str(jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm))
