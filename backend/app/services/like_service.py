"""点赞服务 - 处理文章点赞/取消点赞逻辑"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.article import Article
from app.models.like import Like


class LikeService:
    """点赞服务类 - 封装点赞切换和查询操作"""

    @staticmethod
    async def toggle_like(db: AsyncSession, user_id: int, article_id: int) -> bool:
        """切换点赞状态 - 已点赞则取消，未点赞则添加。返回True表示点赞，False表示取消"""
        result = await db.execute(
            select(Like).where(Like.user_id == user_id, Like.article_id == article_id)
        )
        existing = result.scalar_one_or_none()

        # 获取文章用于更新点赞计数
        article_result = await db.execute(select(Article).where(Article.id == article_id))
        article = article_result.scalar_one_or_none()

        if existing:
            # 已点赞，取消点赞并减少计数
            await db.delete(existing)
            if article:
                article.like_count = max(0, article.like_count - 1)  # 防止计数为负
            await db.commit()
            return False
        else:
            # 未点赞，添加点赞记录并增加计数
            like = Like(user_id=user_id, article_id=article_id)
            db.add(like)
            if article:
                article.like_count += 1
            await db.commit()
            return True

    @staticmethod
    async def is_liked(db: AsyncSession, user_id: int, article_id: int) -> bool:
        """检查用户是否已对文章点赞"""
        result = await db.execute(
            select(Like).where(Like.user_id == user_id, Like.article_id == article_id)
        )
        return result.scalar_one_or_none() is not None
