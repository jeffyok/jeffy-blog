"""
数据库会话模块
创建异步引擎、会话工厂和依赖注入函数
"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# 创建异步数据库引擎
async_engine = create_async_engine(settings.DATABASE_URL, echo=False)
# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    """所有 ORM 模型的基类"""
    pass


async def get_db():
    """FastAPI 依赖：获取数据库会话，请求结束后自动关闭"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
