import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from uuid import UUID

import bcrypt
from sqlalchemy import select

from fipilot.database import database_session
from fipilot.models import AuthSession, User

SESSION_COOKIE_NAME = "fipilot_session"
SESSION_TTL = timedelta(days=30)


def normalize_email(email: str) -> str:
    return email.strip().lower()


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("ascii")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("ascii"))
    except (ValueError, TypeError):
        return False


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def create_user(email: str, full_name: str, password: str) -> User:
    with database_session() as db:
        if db is None:
            raise RuntimeError("Database is not configured")
        normalized = normalize_email(email)
        if db.scalar(select(User).where(User.email == normalized)) is not None:
            raise ValueError("An account with this email already exists")
        user = User(email=normalized, full_name=full_name.strip(), password_hash=hash_password(password))
        db.add(user)
        db.flush()
        return user


def authenticate(email: str, password: str) -> User | None:
    with database_session() as db:
        if db is None:
            raise RuntimeError("Database is not configured")
        user = db.scalar(select(User).where(User.email == normalize_email(email)))
        if user is None or not verify_password(password, user.password_hash):
            return None
        return user


def create_session(user_id: UUID) -> str:
    token = secrets.token_urlsafe(48)
    with database_session() as db:
        if db is None:
            raise RuntimeError("Database is not configured")
        db.add(
            AuthSession(
                user_id=user_id,
                token_hash=_hash_token(token),
                expires_at=datetime.now(timezone.utc) + SESSION_TTL,
            )
        )
    return token


def get_user_from_token(token: str | None) -> User | None:
    if not token:
        return None
    with database_session() as db:
        if db is None:
            raise RuntimeError("Database is not configured")
        auth_session = db.scalar(
            select(AuthSession).where(
                AuthSession.token_hash == _hash_token(token),
                AuthSession.expires_at > datetime.now(timezone.utc),
            )
        )
        return db.get(User, auth_session.user_id) if auth_session is not None else None


def revoke_token(token: str | None) -> None:
    if not token:
        return
    with database_session() as db:
        if db is None:
            return
        auth_session = db.scalar(select(AuthSession).where(AuthSession.token_hash == _hash_token(token)))
        if auth_session is not None:
            db.delete(auth_session)
