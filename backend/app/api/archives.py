"""
归档 API 路由
按年月分组返回已发布文章列表
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.archive_service import ArchiveService

router = APIRouter(prefix="/api", tags=["archives"])


@router.get("/archives")
async def get_archives(db: AsyncSession = Depends(get_db)):
    """获取文章归档（按年/月分组）"""
    return {"archives": await ArchiveService.get_archives(db)}
