# -*- coding: utf-8 -*-
"""
安全模块
提供密码哈希、密码校验和 JWT 令牌的生成与解析功能
"""

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import settings


def hash_password(password: str) -> str:
    """
    使用 bcrypt 对明文密码进行哈希
    :param password: 明文密码
    :return: bcrypt 哈希字符串
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """
    校验明文密码是否与哈希值匹配
    :param plain: 明文密码
    :param hashed: bcrypt 哈希值
    :return: 匹配返回 True，否则 False
    """
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    生成 JWT 访问令牌
    :param data: 令牌载荷数据，通常包含 sub 字段（用户ID）
    :param expires_delta: 过期时间间隔，默认使用配置中的 ACCESS_TOKEN_EXPIRE_MINUTES
    :return: JWT 令牌字符串
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
    """
    解析 JWT 令牌，返回载荷字典
    :param token: JWT 令牌字符串
    :return: 载荷字典
    :raises jwt.JWTError: 令牌无效或过期时抛出
    """
    # 不验证 subject 必须是字符串的要求，因为旧 token 的 sub 可能是数字
    options = {"verify_sub": False}
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM], options=options)
