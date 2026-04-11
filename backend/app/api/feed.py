"""
RSS 订阅源 API 路由
生成 RSS 2.0 格式的订阅源，包含最新 20 篇已发布文章
"""

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_db
from app.services.article_service import ArticleService

router = APIRouter(prefix="/api/feed", tags=["feed"])


@router.get("/rss")
async def rss_feed(db: AsyncSession = Depends(get_db)):
    """生成 RSS 订阅源"""
    from feedgen.feed import FeedGenerator

    # 初始化 Feed
    fg = FeedGenerator()
    fg.title("Jeffy Blog")
    fg.link(href=settings.SITE_URL, rel="alternate")
    fg.description("个人博客")
    fg.language("zh-CN")

    # 取最新 20 篇已发布文章
    articles, _ = await ArticleService.get_articles(db, status="published", page=1, page_size=20)
    for article in articles:
        fe = fg.add_entry()
        fe.id(f"{settings.SITE_URL}/article/{article.slug}")
        fe.title(article.title)
        fe.published(article.created_at)
        fe.content(article.content_html or article.content, type="html")

    return Response(content=fg.rss_str(), media_type="application/rss+xml")
