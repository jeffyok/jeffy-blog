"""
评论服务 - 处理评论的增删改查业务逻辑
"""

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.comment import Comment
from app.schemas.comment import CommentCreate


class CommentService:
    """评论服务类 - 封装评论的创建、查询和管理操作"""

    @staticmethod
    async def create_comment(
        db: AsyncSession,
        article_id: int,
        data: CommentCreate,
        user_id: int | None = None,
    ) -> Comment:
        """
        创建评论
        :param article_id: 文章ID
        :param data: 评论数据（内容、父评论ID、游客昵称和邮箱）
        :param user_id: 登录用户ID，游客评论时为None
        :return: 创建的评论对象
        """
        comment = Comment(
            content=data.content,
            article_id=article_id,
            user_id=user_id,
            nickname=data.nickname,
            email=data.email,
            parent_id=data.parent_id,
        )
        db.add(comment)
        await db.commit()
        await db.refresh(comment)
        return comment

    @staticmethod
    async def get_comments_by_article(db: AsyncSession, article_id: int) -> list[Comment]:
        """
        获取文章的评论列表（扁平结构，按创建时间排序）
        返回所有已审核的评论
        """
        result = await db.execute(
            select(Comment)
            .options(selectinload(Comment.user))  # 预加载关联的用户数据
            .where(Comment.article_id == article_id, Comment.status == "approved")
            .order_by(Comment.created_at)
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_all_comments(
        db: AsyncSession,
        page: int = 1,
        page_size: int = 20,
        status: str | None = None,
    ) -> tuple[list[Comment], int]:
        """
        管理员获取所有评论（分页，支持按状态过滤）
        :return: (评论列表, 总数)
        """
        query = select(Comment)
        count_query = select(func.count(Comment.id))

        # 按状态筛选（如 pending、approved、rejected）
        if status:
            query = query.where(Comment.status == status)
            count_query = count_query.where(Comment.status == status)

        total = (await db.execute(count_query)).scalar() or 0
        # 按创建时间降序，最新的在前
        query = query.order_by(Comment.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
        result = await db.execute(query)
        return list(result.scalars().all()), total

    @staticmethod
    async def update_comment_status(db: AsyncSession, comment_id: int, status: str) -> Comment | None:
        """
        更新评论状态（审核通过/拒绝）
        :return: 更新后的评论，不存在时返回None
        """
        result = await db.execute(select(Comment).where(Comment.id == comment_id))
        comment = result.scalar_one_or_none()
        if not comment:
            return None
        comment.status = status
        await db.commit()
        await db.refresh(comment)
        return comment

    @staticmethod
    async def delete_comment(db: AsyncSession, comment: Comment) -> None:
        """删除评论"""
        await db.delete(comment)
        await db.commit()
