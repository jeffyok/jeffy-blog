"""评论模型"""

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.base import TimestampMixin


class Comment(Base, TimestampMixin):
    """评论模型 - 支持嵌套回复的评论系统"""

    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)  # 主键
    content: Mapped[str] = mapped_column(Text)  # 评论内容
    article_id: Mapped[int] = mapped_column(ForeignKey("articles.id", ondelete="CASCADE"))  # 所属文章ID，级联删除
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))  # 评论者用户ID，用户删除时置空
    nickname: Mapped[str | None] = mapped_column(String(50))  # 游客评论昵称
    email: Mapped[str | None] = mapped_column(String(255))  # 游客评论邮箱
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("comments.id", ondelete="CASCADE"))  # 父评论ID，支持嵌套回复
    status: Mapped[str] = mapped_column(String(20), default="approved")  # 状态：approved/pending/spam

    # 关联关系
    article: Mapped["Article"] = relationship(back_populates="comments")  # 所属文章
    user: Mapped["User | None"] = relationship()  # 评论者
    parent: Mapped["Comment | None"] = relationship(remote_side="Comment.id", back_populates="replies")  # 父评论
    replies: Mapped[list["Comment"]] = relationship(back_populates="parent", cascade="all, delete-orphan")  # 子回复列表，级联删除
