"""
管理端 - 标签管理 API 路由
标签的创建、更新、删除（需管理员权限）
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_admin
from app.db.session import get_db
from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagUpdate
from app.schemas.article import TagOut
from app.services.tag_service import TagService

router = APIRouter(prefix="/api/admin/tags", tags=["admin-tags"])


@router.get("/", response_model=list[TagOut])
async def list_tags(db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    """获取所有标签列表（需管理员权限）"""
    return await TagService.get_tags(db)


@router.post("/", response_model=TagOut, status_code=201)
async def create_tag(data: TagCreate, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    """创建新标签（需管理员权限）"""
    return await TagService.create_tag(db, data)


@router.put("/{tag_id}", response_model=TagOut)
async def update_tag(tag_id: int, data: TagUpdate, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    """更新标签（需管理员权限）"""
    result = await db.execute(select(Tag).where(Tag.id == tag_id))
    tag = result.scalar_one_or_none()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return await TagService.update_tag(db, tag, data)


@router.delete("/{tag_id}", status_code=204)
async def delete_tag(tag_id: int, db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    """删除标签（需管理员权限）"""
    result = await db.execute(select(Tag).where(Tag.id == tag_id))
    tag = result.scalar_one_or_none()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    await TagService.delete_tag(db, tag)
