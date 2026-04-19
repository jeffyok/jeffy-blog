"""
管理端 - 文章管理 API 路由
文章的列表查询、创建、更新、删除（需管理员权限）
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.article import ArticleCreate, ArticlePaginationOut, ArticleUpdate
from app.services.article_service import ArticleService

router = APIRouter(prefix="/api/admin/articles", tags=["admin-articles"])


@router.get("/", response_model=ArticlePaginationOut)
async def list_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    category_id: int | None = None,
    tag_id: int | None = None,
    search: str | None = None,
    status: str | None = None,
    db: AsyncSession = Depends(get_db),
    _=Depends(require_admin),
):
    """获取文章列表（分页，支持分类/标签/搜索/状态过滤，需管理员权限）"""
    articles, total = await ArticleService.get_articles_with_details(
        db, page=page, page_size=page_size, category_id=category_id, tag_id=tag_id, search=search, status=status
    )
    return ArticlePaginationOut(items=articles, total=total, page=page, page_size=page_size)


@router.post("/", status_code=201)
async def create_article(
    data: ArticleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """创建新文章（需管理员权限）"""
    article = await ArticleService.create_article(db, data, current_user.id)
    return await ArticleService.get_article_detail_with_details(db, article)


@router.put("/{article_id}")
async def update_article(
    article_id: int,
    data: ArticleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
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
    current_user: User = Depends(require_admin),
):
    """删除文章（需管理员权限）"""
    article = await ArticleService.get_article_by_id(db, article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    await ArticleService.delete_article(db, article)
