"""友情链接服务 - 处理友情链接的增删改查业务逻辑"""

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.friend_link import FriendLink
from app.schemas.friend_link import FriendLinkCreate, FriendLinkUpdate


class FriendLinkService:
    """友情链接服务类 - 封装友情链接的CRUD操作"""

    @staticmethod
    async def get_friend_links(db: AsyncSession) -> list[FriendLink]:
        """获取所有友情链接，按排序权重和ID排序"""
        result = await db.execute(select(FriendLink).order_by(FriendLink.sort_order, FriendLink.id))
        return list(result.scalars().all())

    @staticmethod
    async def create_friend_link(db: AsyncSession, data: FriendLinkCreate) -> FriendLink:
        """创建友情链接"""
        link = FriendLink(**data.model_dump())
        db.add(link)
        await db.commit()
        await db.refresh(link)
        return link

    @staticmethod
    async def update_friend_link(db: AsyncSession, link: FriendLink, data: FriendLinkUpdate) -> FriendLink:
        """更新友情链接 - 仅更新非None字段"""
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(link, key, value)
        await db.commit()
        await db.refresh(link)
        return link

    @staticmethod
    async def delete_friend_link(db: AsyncSession, link: FriendLink) -> None:
        """删除友情链接"""
        await db.delete(link)
        await db.commit()
