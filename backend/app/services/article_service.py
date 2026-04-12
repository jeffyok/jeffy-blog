"""文章服务 - 处理文章的增删改查业务逻辑"""

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.article import Article
from app.models.tag import Tag, article_tags
from app.schemas.article import ArticleCreate, ArticleUpdate
from app.utils.markdown import render_markdown, extract_summary
from app.utils.slug import generate_slug


class ArticleService:
    """文章服务类 - 封装文章的CRUD及查询操作"""

    @staticmethod
    async def create_article(db: AsyncSession, data: ArticleCreate, author_id: int) -> Article:
        """创建文章 - 自动生成slug、渲染HTML、提取摘要"""
        # 生成URL标识，未指定时从标题自动生成
        slug = data.slug or generate_slug(data.title)
        # 检查slug唯一性，冲突时追加随机后缀
        existing = await db.execute(select(Article).where(Article.slug == slug))
        if existing.scalar_one_or_none():
            slug = slug + "-" + generate_slug("").hex[:4]

        article = Article(
            title=data.title,
            slug=slug,
            content=data.content,
            content_html=render_markdown(data.content),  # Markdown转HTML
            summary=data.summary or extract_summary(data.content),  # 自动提取摘要
            cover_image=data.cover_image,
            category_id=data.category_id,
            author_id=author_id,
            status=data.status,
            is_top=data.is_top,
        )

        # 关联标签
        if data.tag_ids:
            result = await db.execute(select(Tag).where(Tag.id.in_(data.tag_ids)))
            article.tags = list(result.scalars().all())

        db.add(article)
        await db.commit()
        await db.refresh(article)
        return article

    @staticmethod
    async def get_articles(
        db: AsyncSession,
        page: int = 1,
        page_size: int = 10,
        category_id: int | None = None,
        tag_id: int | None = None,
        search: str | None = None,
        status: str | None = None,
    ) -> tuple[list[Article], int]:
        """分页查询文章列表 - 支持按分类、标签、关键词筛选"""
        print(f"[DEBUG] get_articles called with status={repr(status)}, type={type(status)}")
        # 构建主查询，预加载关联的category、tags、author
        query = select(Article).options(
            selectinload(Article.category),
            selectinload(Article.tags),
            selectinload(Article.author),
        )

        # 构建计数查询
        count_query = select(func.count(Article.id))

        # 按状态筛选
        if status:
            print(f"[DEBUG] Filtering by status: {status}")
            query = query.where(Article.status == status)
            count_query = count_query.where(Article.status == status)
            print(f"[DEBUG] Query after status filter: {str(query)[:200]}")
        # 按分类筛选
        if category_id:
            query = query.where(Article.category_id == category_id)
            count_query = count_query.where(Article.category_id == category_id)
        # 按标签筛选（需通过关联表join）
        if tag_id:
            query = query.join(article_tags).where(article_tags.c.tag_id == tag_id)
            count_query = count_query.join(article_tags).where(article_tags.c.tag_id == tag_id)
        # 按标题关键词搜索
        if search:
            search_filter = Article.title.ilike(f"%{search}%")
            query = query.where(search_filter)
            count_query = count_query.where(search_filter)

        # 获取总数
        total = (await db.execute(count_query)).scalar() or 0
        print(f"[DEBUG] Total count: {total}")

        # 排序：置顶优先，然后按创建时间降序
        query = query.order_by(Article.is_top.desc(), Article.created_at.desc())
        # 分页偏移
        query = query.offset((page - 1) * page_size).limit(page_size)

        print(f"[DEBUG] Final query: {str(query)[:300]}...")
        result = await db.execute(query)
        articles = list(result.scalars().all())
        print(f"[DEBUG] Result count: {len(articles)}")
        for article in articles:
            print(f"[DEBUG] Article ID: {article.id}, Title: {article.title[:30]}, Status: {article.status}")
        return articles, total

    @staticmethod
    async def get_article_by_slug(db: AsyncSession, slug: str) -> Article | None:
        """根据slug查询文章详情"""
        result = await db.execute(
            select(Article)
            .options(
                selectinload(Article.category),
                selectinload(Article.tags),
                selectinload(Article.author),
            )
            .where(Article.slug == slug)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_article_by_id(db: AsyncSession, article_id: int) -> Article | None:
        """根据ID查询文章详情"""
        result = await db.execute(
            select(Article)
            .options(
                selectinload(Article.category),
                selectinload(Article.tags),
                selectinload(Article.author),
            )
            .where(Article.id == article_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def update_article(db: AsyncSession, article: Article, data: ArticleUpdate) -> Article:
        """更新文章 - 处理标签关联和内容渲染"""
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if key == "tag_ids" and value is not None:
                # 更新标签关联
                result = await db.execute(select(Tag).where(Tag.id.in_(value)))
                article.tags = list(result.scalars().all())
            elif key == "content" and value is not None:
                # 更新内容时同步重新渲染HTML和摘要
                article.content = value
                article.content_html = render_markdown(value)
                article.summary = article.summary or extract_summary(value)
            else:
                setattr(article, key, value)

        # 检查slug唯一性（排除自身）
        if data.slug:
            existing = await db.execute(select(Article).where(Article.slug == data.slug, Article.id != article.id))
            if existing.scalar_one_or_none():
                raise HTTPException(status_code=400, detail="Slug already exists")

        await db.commit()
        await db.refresh(article)
        return article

    @staticmethod
    async def delete_article(db: AsyncSession, article: Article) -> None:
        """删除文章"""
        await db.delete(article)
        await db.commit()

    @staticmethod
    async def increment_view_count(db: AsyncSession, article: Article) -> None:
        """增加文章浏览量"""
        article.view_count += 1
        await db.commit()
