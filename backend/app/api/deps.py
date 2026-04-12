"""
API 共享依赖
提供数据库会话、用户认证、管理员权限等依赖注入函数
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User
from app.services.auth_service import AuthService

# 使用 HTTPBearer 而不是 OAuth2PasswordBearer，直接从 Authorization header 提取 token
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    依赖：从 JWT 令牌中解析当前登录用户
    失败时抛出 401 异常
    """
    token = credentials.credentials
    import sys
    print(f"[DEBUG] Received token (first 50 chars): {token[:50]}...")
    print(f"[DEBUG] Token length: {len(token)}")
    try:
        payload = decode_access_token(token)
        print(f"[DEBUG] Decoded payload: {payload}")
        user_id = payload.get("sub")
        print(f"[DEBUG] user_id from payload: {user_id}, type: {type(user_id)}")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token: no sub")
        # JWT payload 中的 sub 可能是字符串或数字，需要转换为整数
        try:
            user_id = int(user_id)
            print(f"[DEBUG] Converted user_id to int: {user_id}")
        except (ValueError, TypeError) as e:
            print(f"[DEBUG] Failed to convert user_id to int: {e}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token: invalid user_id")
    except HTTPException:
        raise
    except Exception as e:
        print(f"[DEBUG] Token decode error: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = await AuthService.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """依赖：要求当前用户必须为管理员，否则抛出 403 异常"""
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user
