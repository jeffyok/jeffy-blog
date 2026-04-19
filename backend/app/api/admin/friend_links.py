"""
管理端 - 友情链接管理 API 路由
友链的创建、更新、删除（需管理员权限）
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_admin
from app.db.session import get_db
from app.models.friend_link import FriendLink
from app.schemas.friend_link import FriendLinkCreate, FriendLinkOut, FriendLinkUpdate
from app.services.friend_link_service import FriendLinkService

router = APIRouter(prefix="/api/admin/friend-links", tags=["admin-friend-links"])


@router.post("/", response_model=FriendLinkOut, status_code=201)
async def create_friend_link(data: FriendLinkCreate, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    """创建友情链接（需管理员权限）"""
    return await FriendLinkService.create_friend_link(db, data)


@router.put("/{link_id}", response_model=FriendLinkOut)
async def update_friend_link(link_id: int, data: FriendLinkUpdate, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    """更新友情链接（需管理员权限）"""
    result = await db.execute(select(FriendLink).where(FriendLink.id == link_id))
    link = result.scalar_one_or_none()
    if not link:
        raise HTTPException(status_code=404, detail="Friend link not found")
    return await FriendLinkService.update_friend_link(db, link, data)


@router.delete("/{link_id}", status_code=204)
async def delete_friend_link(link_id: int, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    """删除友情链接（需管理员权限）"""
    result = await db.execute(select(FriendLink).where(FriendLink.id == link_id))
    link = result.scalar_one_or_none()
    if not link:
        raise HTTPException(status_code=404, detail="Friend link not found")
    await FriendLinkService.delete_friend_link(db, link)
