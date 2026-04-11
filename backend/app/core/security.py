"""
安全模块
提供密码哈希、验证和 JWT 令牌的创建与解析
"""

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import settings


def hash_password(password: str) -> str:
    """对明文密码进行 bcrypt 哈希，返回哈希字符串"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """验证明文密码是否与哈希匹配"""
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    创建 JWT 访问令牌
    :param data: 载荷数据（通常包含 sub 字段存储用户 ID）
    :param expires_delta: 过期时间间隔，默认使用配置中的值
    :return: JWT 令牌字符串
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict:
    """解析 JWT 令牌，返回载荷字典（失败时抛出 JWTError）"""
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
