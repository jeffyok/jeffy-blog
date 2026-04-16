"""文章服务 - 处理文章的增删改查业务逻辑"""

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.article import Article
from app.models.category import Category
from app.models.user import User
from app.models.tag import Tag, article_tags
from app.schemas.article import ArticleCreate, ArticleListOut, ArticleUpdate
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

        db.add(article)
        await db.flush()  # 获取article.id

        # 手动插入标签关联记录
        if data.tag_ids:
            for tag_id in data.tag_ids:
                await db.execute(
                    article_tags.insert().values(article_id=article.id, tag_id=tag_id)
                )

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
        # 构建主查询
        query = select(Article)

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
        result = await db.execute(select(Article).where(Article.slug == slug))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_article_by_id(db: AsyncSession, article_id: int) -> Article | None:
        """根据ID查询文章详情"""
        result = await db.execute(select(Article).where(Article.id == article_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def update_article(db: AsyncSession, article: Article, data: ArticleUpdate) -> Article:
        """更新文章 - 处理标签关联和内容渲染"""
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if key == "tag_ids" and value is not None:
                # 手动更新标签关联：先删除旧的，再插入新的
                await db.execute(article_tags.delete().where(article_tags.c.article_id == article.id))
                for tag_id in value:
                    await db.execute(
                        article_tags.insert().values(article_id=article.id, tag_id=tag_id)
                    )
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

    @staticmethod
    async def get_articles_with_details(
        db: AsyncSession,
        page: int = 1,
        page_size: int = 10,
        category_id: int | None = None,
        tag_id: int | None = None,
        search: str | None = None,
        status: str | None = None,
    ) -> tuple[list[dict], int]:
        """分页查询文章列表并组装关联数据（分类、标签、作者）"""
        # 1. 查询文章（复用现有逻辑）
        articles, total = await ArticleService.get_articles(
            db, page=page, page_size=page_size, category_id=category_id, tag_id=tag_id, search=search, status=status
        )

        if not articles:
            return [], total

        # 2. 批量查询关联数据
        category_ids = {a.category_id for a in articles if a.category_id}
        author_ids = {a.author_id for a in articles}
        article_ids = [a.id for a in articles]

        # 3. 查询categories
        categories_dict = {}
        if category_ids:
            result = await db.execute(select(Category).where(Category.id.in_(category_ids)))
            categories = result.scalars().all()
            categories_dict = {c.id: c for c in categories}

        # 4. 查询authors (users)
        authors_dict = {}
        if author_ids:
            result = await db.execute(select(User).where(User.id.in_(author_ids)))
            authors = result.scalars().all()
            authors_dict = {u.id: u for u in authors}

        # 5. 查询文章-标签关联
        article_tags_map = {}
        tag_ids_set = set()
        if article_ids:
            result = await db.execute(
                select(article_tags.c.article_id, article_tags.c.tag_id)
                .where(article_tags.c.article_id.in_(article_ids))
            )
            for article_id, tag_id in result.all():
                if article_id not in article_tags_map:
                    article_tags_map[article_id] = []
                article_tags_map[article_id].append(tag_id)
                tag_ids_set.add(tag_id)

        # 6. 查询tags
        tags_dict = {}
        if tag_ids_set:
            result = await db.execute(select(Tag).where(Tag.id.in_(tag_ids_set)))
            tags = result.scalars().all()
            tags_dict = {t.id: t for t in tags}

        # 7. 组装返回字典列表（包含完整关联对象）
        result_list = []
        for article in articles:
            result_list.append({
                "id": article.id,
                "title": article.title,
                "slug": article.slug,
                "summary": article.summary,
                "cover_image": article.cover_image,
                "category": categories_dict.get(article.category_id),
                "tags": [tags_dict[tid] for tid in article_tags_map.get(article.id, []) if tid in tags_dict],
                "author": authors_dict.get(article.author_id),
                "status": article.status,
                "is_top": article.is_top,
                "view_count": article.view_count,
                "like_count": article.like_count,
                "created_at": article.created_at,
                "updated_at": article.updated_at,
            })

        return result_list, total

    @staticmethod
    async def get_article_detail_with_details(db: AsyncSession, article: Article) -> dict:
        """获取文章详情并组装关联数据"""
        # 查询category
        category = None
        if article.category_id:
            result = await db.execute(select(Category).where(Category.id == article.category_id))
            category = result.scalar_one_or_none()

        # 查询author (user)
        result = await db.execute(select(User).where(User.id == article.author_id))
        author = result.scalar_one_or_none()

        # 查询tags
        tag_ids = []
        tags = []
        if article.id:
            result = await db.execute(
                select(article_tags.c.tag_id).where(article_tags.c.article_id == article.id)
            )
            tag_ids = [row[0] for row in result.all()]

        # 批量查询tags
        if tag_ids:
            result = await db.execute(select(Tag).where(Tag.id.in_(tag_ids)))
            tags = list(result.scalars().all())

        # 组装返回字典（包含完整关联对象）
        return {
            "id": article.id,
            "title": article.title,
            "slug": article.slug,
            "content": article.content,
            "content_html": article.content_html,
            "summary": article.summary,
            "cover_image": article.cover_image,
            "category": category,
            "tags": tags,
            "author": author,
            "status": article.status,
            "is_top": article.is_top,
            "view_count": article.view_count,
            "like_count": article.like_count,
            "created_at": article.created_at,
            "updated_at": article.updated_at,
        }
