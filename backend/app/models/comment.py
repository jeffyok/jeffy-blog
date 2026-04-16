# -*- coding: utf-8 -*-
"""评论模型"""

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.base import TimestampMixin


class Comment(Base, TimestampMixin):
    """评论模型 - 支持嵌套回复的评论系统"""

    __tablename__ = "comments"
    __table_args__ = {"comment": "文章评论表"}

    id: Mapped[int] = mapped_column(primary_key=True, comment="主键ID")
    content: Mapped[str] = mapped_column(Text, comment="评论内容")
    article_id: Mapped[int] = mapped_column(comment="所属文章ID")
    user_id: Mapped[int | None] = mapped_column(comment="评论者用户ID，用户删除时置空")
    nickname: Mapped[str | None] = mapped_column(String(50), comment="游客评论昵称")
    email: Mapped[str | None] = mapped_column(String(255), comment="游客评论邮箱")
    parent_id: Mapped[int | None] = mapped_column(comment="父评论ID，支持嵌套回复")
    status: Mapped[str] = mapped_column(String(20), default="approved", comment="状态：approved-已审核，pending-待审核，spam-垃圾评论")

    # 关联关系：由于不使用数据库外键，改为在 Service 层手动查询
