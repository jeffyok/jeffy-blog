# -*- coding: utf-8 -*-
"""
Security module
Provides password hashing, verification and JWT token creation/parsing
"""

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import settings


def hash_password(password: str) -> str:
    """Hash plain password with bcrypt, return hash string"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """Verify plain password matches hash"""
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create JWT access token
    :param data: payload data (usually contains sub field for user ID)
    :param expires_delta: expiry interval, defaults to config value
    :return: JWT token string
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    import sys
    print(f"[DEBUG] Creating token with sub type: {type(to_encode.get('sub'))}, value: {to_encode.get('sub')}", file=sys.stderr, flush=True)
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    print(f"[DEBUG] Token created: {token[:50]}...", file=sys.stderr, flush=True)
    return token


def decode_access_token(token: str) -> dict:
    """Parse JWT token, return payload dict (raises JWTError on failure)"""
    # 不验证 subject 必须是字符串的要求，因为旧 token 可能是数字
    options = {"verify_sub": False}
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM], options=options)
