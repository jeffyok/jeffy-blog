"""标签服务 - 处理标签的增删改查业务逻辑"""

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.article import Article
from app.models.tag import Tag, article_tags
from app.schemas.tag import TagCreate, TagUpdate
from app.utils.slug import generate_slug


class TagService:
    """标签服务类 - 封装标签的CRUD及统计操作"""

    @staticmethod
    async def create_tag(db: AsyncSession, data: TagCreate) -> Tag:
        """创建标签 - 自动生成slug，检查唯一性"""
        slug = data.slug or generate_slug(data.name)
        existing = await db.execute(select(Tag).where(Tag.slug == slug))
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Tag slug already exists")
        tag = Tag(name=data.name, slug=slug)
        db.add(tag)
        await db.commit()
        await db.refresh(tag)
        return tag

    @staticmethod
    async def get_tags(db: AsyncSession) -> list[Tag]:
        """获取所有标签，按ID排序"""
        result = await db.execute(select(Tag).order_by(Tag.id))
        return list(result.scalars().all())

    @staticmethod
    async def get_tag_by_slug(db: AsyncSession, slug: str) -> Tag | None:
        """根据slug查询标签"""
        result = await db.execute(select(Tag).where(Tag.slug == slug))
        return result.scalar_one_or_none()

    @staticmethod
    async def update_tag(db: AsyncSession, tag: Tag, data: TagUpdate) -> Tag:
        """更新标签 - 仅更新非None字段"""
        if data.name is not None:
            tag.name = data.name
        if data.slug is not None:
            tag.slug = data.slug
        await db.commit()
        await db.refresh(tag)
        return tag

    @staticmethod
    async def delete_tag(db: AsyncSession, tag: Tag) -> None:
        """删除标签"""
        await db.delete(tag)
        await db.commit()

    @staticmethod
    async def get_tag_with_count(db: AsyncSession, tag_id: int) -> dict:
        """获取标签关联的文章数量 - 通过关联表统计"""
        result = await db.execute(
            select(func.count(article_tags.c.article_id)).where(article_tags.c.tag_id == tag_id)
        )
        count = result.scalar() or 0
        return {"count": count}
