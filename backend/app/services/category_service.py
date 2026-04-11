"""分类服务 - 处理分类的增删改查业务逻辑"""

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.article import Article
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.utils.slug import generate_slug


class CategoryService:
    """分类服务类 - 封装分类的CRUD及统计操作"""

    @staticmethod
    async def create_category(db: AsyncSession, data: CategoryCreate) -> Category:
        """创建分类 - 自动生成slug，检查唯一性"""
        slug = data.slug or generate_slug(data.name)
        existing = await db.execute(select(Category).where(Category.slug == slug))
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Category slug already exists")
        category = Category(name=data.name, slug=slug, description=data.description)
        db.add(category)
        await db.commit()
        await db.refresh(category)
        return category

    @staticmethod
    async def get_categories(db: AsyncSession) -> list[Category]:
        """获取所有分类，按ID排序"""
        result = await db.execute(select(Category).order_by(Category.id))
        return list(result.scalars().all())

    @staticmethod
    async def get_category_by_slug(db: AsyncSession, slug: str) -> Category | None:
        """根据slug查询分类"""
        result = await db.execute(select(Category).where(Category.slug == slug))
        return result.scalar_one_or_none()

    @staticmethod
    async def update_category(db: AsyncSession, category: Category, data: CategoryUpdate) -> Category:
        """更新分类 - 仅更新非None字段"""
        if data.name is not None:
            category.name = data.name
        if data.slug is not None:
            category.slug = data.slug
        if data.description is not None:
            category.description = data.description
        await db.commit()
        await db.refresh(category)
        return category

    @staticmethod
    async def delete_category(db: AsyncSession, category: Category) -> None:
        """删除分类"""
        await db.delete(category)
        await db.commit()

    @staticmethod
    async def get_category_with_count(db: AsyncSession, category_id: int) -> dict:
        """获取分类下的文章数量"""
        result = await db.execute(
            select(func.count(Article.id)).where(Article.category_id == category_id)
        )
        count = result.scalar() or 0
        return {"count": count}
