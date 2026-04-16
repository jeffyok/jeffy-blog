"""
文章相关 API 路由
包含文章的列表查询、详情获取、创建、更新、删除
公开接口：列表和详情；管理接口：创建、更新、删除（需管理员权限）
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.article import (
    ArticleCreate,
    ArticleOut,
    ArticlePaginationOut,
    ArticleUpdate,
)
from app.services.article_service import ArticleService

router = APIRouter(prefix="/api/articles", tags=["articles"])


@router.get("/", response_model=ArticlePaginationOut)
async def list_articles(
    page: int = Query(1, ge=1),              # 当前页码
    page_size: int = Query(10, ge=1, le=50), # 每页条数
    category_id: int | None = None,          # 按分类过滤
    tag_id: int | None = None,               # 按标签过滤
    search: str | None = None,               # 搜索关键词
    status: str | None = None,               # 状态过滤：不传则返回所有状态
    db: AsyncSession = Depends(get_db),
):
    """获取文章列表（分页，支持分类/标签/搜索过滤）"""
    print(f"[DEBUG API] Received status={repr(status)}, type={type(status)}")
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


@router.post("/", status_code=201)
async def create_article(
    data: ArticleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),  # 仅管理员可创建
):
    """创建新文章（需管理员权限）"""
    article = await ArticleService.create_article(db, data, current_user.id)
    return await ArticleService.get_article_detail_with_details(db, article)


@router.put("/{article_id}")
async def update_article(
    article_id: int,
    data: ArticleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),  # 仅管理员可更新
):
    """更新文章（需管理员权限）"""
    article = await ArticleService.get_article_by_id(db, article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    article = await ArticleService.update_article(db, article, data)
    return await ArticleService.get_article_detail_with_details(db, article)


@router.delete("/{article_id}", status_code=204)
async def delete_article(
    article_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),  # 仅管理员可删除
):
    """删除文章（需管理员权限）"""
    article = await ArticleService.get_article_by_id(db, article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    await ArticleService.delete_article(db, article)
