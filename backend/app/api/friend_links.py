"""
友情链接 API 路由
获取列表为公开接口，管理端 CRUD 需管理员权限
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_admin
from app.db.session import get_db
from app.models.friend_link import FriendLink
from app.schemas.friend_link import FriendLinkCreate, FriendLinkOut, FriendLinkUpdate
from app.services.friend_link_service import FriendLinkService

router = APIRouter(prefix="/api", tags=["friend-links"])


@router.get("/friend-links", response_model=list[FriendLinkOut])
async def list_friend_links(db: AsyncSession = Depends(get_db)):
    """获取友情链接列表（前台公开）"""
    return await FriendLinkService.get_friend_links(db)


@router.post("/admin/friend-links", response_model=FriendLinkOut, status_code=201)
async def create_friend_link(data: FriendLinkCreate, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    """创建友情链接（需管理员权限）"""
    return await FriendLinkService.create_friend_link(db, data)


@router.put("/admin/friend-links/{link_id}", response_model=FriendLinkOut)
async def update_friend_link(link_id: int, data: FriendLinkUpdate, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    """更新友情链接（需管理员权限）"""
    result = await db.execute(select(FriendLink).where(FriendLink.id == link_id))
    link = result.scalar_one_or_none()
    if not link:
        raise HTTPException(status_code=404, detail="Friend link not found")
    return await FriendLinkService.update_friend_link(db, link, data)


@router.delete("/admin/friend-links/{link_id}", status_code=204)
async def delete_friend_link(link_id: int, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    """删除友情链接（需管理员权限）"""
    result = await db.execute(select(FriendLink).where(FriendLink.id == link_id))
    link = result.scalar_one_or_none()
    if not link:
        raise HTTPException(status_code=404, detail="Friend link not found")
    await FriendLinkService.delete_friend_link(db, link)
