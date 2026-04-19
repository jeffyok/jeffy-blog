"""
C 端 - 点赞 API 路由
点赞切换和查询当前用户是否已点赞（需登录）
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.article import Article
from app.models.user import User
from app.services.like_service import LikeService

router = APIRouter(prefix="/api", tags=["likes"])


@router.post("/articles/{article_id}/like/")
async def toggle_like(
    article_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """切换点赞状态（已点赞则取消，未点赞则点赞）"""
    result = await db.execute(select(Article).where(Article.id == article_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Article not found")
    liked = await LikeService.toggle_like(db, current_user.id, article_id)
    return {"liked": liked}


@router.get("/articles/{article_id}/liked/")
async def check_liked(
    article_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """查询当前用户是否已点赞该文章"""
    liked = await LikeService.is_liked(db, current_user.id, article_id)
    return {"liked": liked}
