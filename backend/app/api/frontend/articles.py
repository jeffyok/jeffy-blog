"""
C 端 - 文章 API 路由
包含文章列表查询、详情获取
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.article import ArticlePaginationOut
from app.services.article_service import ArticleService

router = APIRouter(prefix="/api/articles", tags=["articles"])


@router.get("/", response_model=ArticlePaginationOut)
async def list_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    category_id: int | None = None,
    tag_id: int | None = None,
    search: str | None = None,
    status: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """获取文章列表（分页，支持分类/标签/搜索过滤）"""
    articles, total = await ArticleService.get_articles_with_details(
        db, page=page, page_size=page_size, category_id=category_id, tag_id=tag_id, search=search, status=status
    )
    return ArticlePaginationOut(items=articles, total=total, page=page, page_size=page_size)


@router.get("/{slug}")
async def get_article(slug: str, db: AsyncSession = Depends(get_db)):
    """根据 slug 获取文章详情，同时增加浏览量"""
    article = await ArticleService.get_article_by_slug(db, slug)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    await ArticleService.increment_view_count(db, article)
    return await ArticleService.get_article_detail_with_details(db, article)


@router.get("/id/{article_id}")
async def get_article_by_id(article_id: int, db: AsyncSession = Depends(get_db)):
    """根据 ID 获取文章详情（用于编辑）"""
    article = await ArticleService.get_article_by_id(db, article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return await ArticleService.get_article_detail_with_details(db, article)
