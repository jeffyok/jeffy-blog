"""认证服务 - 处理用户注册、登录及查询"""

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.auth import UserCreate


class AuthService:
    """认证服务类 - 封装用户注册、登录和查询的业务逻辑"""

    @staticmethod
    async def register(db: AsyncSession, user_data: UserCreate) -> User:
        """注册新用户 - 检查用户名和邮箱唯一性，创建用户记录"""
        # 检查用户名是否已存在
        existing = await db.execute(select(User).where(User.username == user_data.username))
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Username already registered")

        # 检查邮箱是否已注册
        existing = await db.execute(select(User).where(User.email == user_data.email))
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already registered")

        # 创建用户，密码进行哈希处理
        user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hash_password(user_data.password),
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def login(db: AsyncSession, username: str, password: str) -> str:
        """用户登录 - 验证凭据并返回JWT令牌"""
        result = await db.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        if user is None or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid username or password")
        if not user.is_active:
            raise HTTPException(status_code=401, detail="User is disabled")
        # 生成JWT令牌，以用户ID作为主题
        token = create_access_token(data={"sub": user.id})
        return token

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
        """根据ID查询用户"""
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
