"""
管理后台 API 路由
提供仪表盘统计数据，需管理员权限
"""

from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_admin
from app.db.session import get_db
from app.models.article import Article
from app.models.comment import Comment
from app.models.user import User

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/dashboard")
async def get_dashboard_stats(db: AsyncSession = Depends(get_db), _=Depends(require_admin)):
    """获取后台仪表盘统计数据（需管理员权限）"""
    # 文章统计
    total_articles = (await db.execute(select(func.count(Article.id)))).scalar() or 0
    published_articles = (await db.execute(select(func.count(Article.id)).where(Article.status == "published"))).scalar() or 0
    draft_articles = (await db.execute(select(func.count(Article.id)).where(Article.status == "draft"))).scalar() or 0
    # 评论统计
    total_comments = (await db.execute(select(func.count(Comment.id)))).scalar() or 0
    pending_comments = (await db.execute(select(func.count(Comment.id)).where(Comment.status == "pending"))).scalar() or 0
    # 互动统计
    total_views = (await db.execute(select(func.sum(Article.view_count)))).scalar() or 0
    total_likes = (await db.execute(select(func.sum(Article.like_count)))).scalar() or 0
    # 用户统计
    total_users = (await db.execute(select(func.count(User.id)))).scalar() or 0

    return {
        "total_articles": total_articles,
        "published_articles": published_articles,
        "draft_articles": draft_articles,
        "total_comments": total_comments,
        "pending_comments": pending_comments,
        "total_views": total_views,
        "total_likes": total_likes,
        "total_users": total_users,
    }
