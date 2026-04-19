"""
C 端 - 标签 API 路由
获取标签列表（公开接口）
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.article import TagOut
from app.services.tag_service import TagService

router = APIRouter(prefix="/api/tags", tags=["tags"])


@router.get("/", response_model=list[TagOut])
async def list_tags(db: AsyncSession = Depends(get_db)):
    """获取所有标签列表"""
    return await TagService.get_tags(db)
