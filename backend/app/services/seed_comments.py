"""
评论种子数据 - 添加示例评论
"""

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.models.comment import Comment
from app.models.article import Article
from app.models.user import User
import asyncio

async def seed_comments():
    """添加示例评论"""
    async with AsyncSessionLocal() as db:
        # 获取第一篇文章和用户
        article_result = await db.execute(select(Article).limit(1))
        article = article_result.scalar_one_or_none()
        if not article:
            print("没有找到文章，请先创建文章")
            return

        user_result = await db.execute(select(User).limit(1))
        user = user_result.scalar_one_or_none()

        # 检查是否已有评论
        count_result = await db.execute(func.count(Comment.id))
        if count_result.scalar() > 0:
            print("评论已存在，跳过创建")
            return

        # 创建顶级评论
        top_comment = Comment(
            content="这是一条示例评论，展示了评论的基本功能。",
            article_id=article.id,
            user_id=user.id if user else None,
            status="approved"
        )
        db.add(top_comment)
        await db.flush()

        # 创建回复评论
        reply_comment = Comment(
            content="这是对第一条评论的回复，展示了嵌套回复功能。",
            article_id=article.id,
            user_id=user.id if user else None,
            parent_id=top_comment.id,
            status="approved"
        )
        db.add(reply_comment)

        # 创建另一条顶级评论
        another_comment = Comment(
            content="这是另一条独立的评论。",
            article_id=article.id,
            user_id=user.id if user else None,
            status="approved"
        )
        db.add(another_comment)

        await db.commit()
        print(f"成功添加 {3} 条示例评论")
        print(f"  文章: {article.title}")
        print(f"  用户: {user.username if user else '匿名'}")

if __name__ == "__main__":
    asyncio.run(seed_comments())