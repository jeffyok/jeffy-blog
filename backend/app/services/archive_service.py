"""归档服务 - 按年月归档已发布的文章"""

from sqlalchemy import select, extract, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.article import Article


class ArchiveService:
    """归档服务类 - 将已发布文章按年月分组归档"""

    @staticmethod
    async def get_archives(db: AsyncSession) -> list[dict]:
        """获取文章归档 - 返回按年份和月份分组的文章列表，时间降序排列"""
        # 查询所有已发布文章，预加载分类信息
        result = await db.execute(
            select(Article)
            .options(selectinload(Article.category))
            .where(Article.status == "published")
            .order_by(Article.created_at.desc())
        )
        articles = list(result.scalars().all())

        # 按年月分组归档
        archives = {}
        for article in articles:
            year = article.created_at.year
            month = article.created_at.month
            if year not in archives:
                archives[year] = {}
            if month not in archives[year]:
                archives[year][month] = []
            archives[year][month].append({
                "id": article.id,
                "title": article.title,
                "slug": article.slug,
                "created_at": article.created_at.isoformat(),
            })

        # 按年份降序、月份降序组装返回结果
        return [
            {
                "year": year,
                "months": [
                    {"month": month, "articles": articles}
                    for month, articles in sorted(months.items(), reverse=True)
                ],
            }
            for year, months in sorted(archives.items(), reverse=True)
        ]
