"""
C 端 - 友情链接 API 路由
获取友情链接列表（公开接口）
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.friend_link import FriendLinkOut
from app.services.friend_link_service import FriendLinkService

router = APIRouter(prefix="/api", tags=["friend-links"])


@router.get("/friend-links/", response_model=list[FriendLinkOut])
async def list_friend_links(db: AsyncSession = Depends(get_db)):
    """获取友情链接列表"""
    return await FriendLinkService.get_friend_links(db)
