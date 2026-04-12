"""
认证相关 API 路由
包含用户注册、登录、获取当前用户信息
"""

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import Token, UserCreate, UserOut
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=201)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """用户注册"""
    user = await AuthService.register(db, user_data)
    return user


@router.post("/login", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """用户登录，使用 OAuth2 密码模式，返回 JWT 令牌"""
    token = await AuthService.login(db, form.username, form.password)
    return Token(access_token=token)


@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    """获取当前登录用户信息（需携带有效令牌）"""
    return current_user


@router.get("/test-token")
async def test_token(token: str):
    """测试 token 解析，用于调试"""
    from app.core.security import decode_access_token
    import sys
    print(f"[TEST] Received token: {token[:50]}...")
    try:
        payload = decode_access_token(token)
        print(f"[TEST] Decoded payload: {payload}")
        return {"success": True, "payload": payload}
    except Exception as e:
        print(f"[TEST] Error: {e}")
        return {"success": False, "error": str(e)}
