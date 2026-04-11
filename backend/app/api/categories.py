"""
分类相关 API 路由
获取分类列表为公开接口，创建/更新/删除需管理员权限
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_admin
from app.db.session import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.schemas.article import CategoryOut
from app.services.category_service import CategoryService

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("/", response_model=list[CategoryOut])
async def list_categories(db: AsyncSession = Depends(get_db)):
    """获取所有分类列表"""
    return await CategoryService.get_categories(db)


@router.post("/", response_model=CategoryOut, status_code=201)
async def create_category(data: CategoryCreate, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    """创建新分类（需管理员权限）"""
    return await CategoryService.create_category(db, data)


@router.put("/{category_id}", response_model=CategoryOut)
async def update_category(category_id: int, data: CategoryUpdate, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    """更新分类（需管理员权限）"""
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return await CategoryService.update_category(db, category, data)


@router.delete("/{category_id}", status_code=204)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    """删除分类（需管理员权限）"""
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    await CategoryService.delete_category(db, category)
