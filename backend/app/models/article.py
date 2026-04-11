"""文章模型"""

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.base import TimestampMixin


class Article(Base, TimestampMixin):
    """文章模型 - 存储博客文章数据"""

    __tablename__ = "articles"
    __table_args__ = {"comment": "文章表"}

    id: Mapped[int] = mapped_column(primary_key=True, comment="主键ID")
    title: Mapped[str] = mapped_column(String(200), comment="文章标题")
    slug: Mapped[str] = mapped_column(String(200), unique=True, index=True, comment="URL友好标识")
    content: Mapped[str] = mapped_column(Text, comment="Markdown原文内容")
    content_html: Mapped[str | None] = mapped_column(Text, comment="渲染后的HTML内容")
    summary: Mapped[str | None] = mapped_column(String(500), comment="文章摘要")
    cover_image: Mapped[str | None] = mapped_column(String(500), comment="封面图片URL")
    category_id: Mapped[int | None] = mapped_column(comment="所属分类ID")
    author_id: Mapped[int] = mapped_column(comment="作者ID")
    status: Mapped[str] = mapped_column(String(20), default="draft", comment="状态：draft-草稿，published-已发布")
    is_top: Mapped[bool] = mapped_column(default=False, comment="是否置顶")
    view_count: Mapped[int] = mapped_column(default=0, comment="浏览量")
    like_count: Mapped[int] = mapped_column(default=0, comment="点赞数")

    # 关联关系
    category: Mapped["Category | None"] = relationship(foreign_keys=[category_id], back_populates="articles")
    author: Mapped["User"] = relationship(foreign_keys=[author_id], back_populates="articles")
    tags: Mapped[list["Tag"]] = relationship(
        secondary="article_tags",
        primaryjoin="Article.id == article_tags.c.article_id",
        secondaryjoin="Tag.id == article_tags.c.tag_id",
        back_populates="articles",
    )
    comments: Mapped[list["Comment"]] = relationship(
        foreign_keys="Comment.article_id",
        back_populates="article",
        cascade="all, delete-orphan",
    )
