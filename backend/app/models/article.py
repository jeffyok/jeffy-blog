"""文章模型"""

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.base import TimestampMixin


class Article(Base, TimestampMixin):
    """文章模型 - 存储博客文章数据"""

    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True)  # 主键
    title: Mapped[str] = mapped_column(String(200))  # 文章标题
    slug: Mapped[str] = mapped_column(String(200), unique=True, index=True)  # URL友好标识，唯一且建索引
    content: Mapped[str] = mapped_column(Text)  # Markdown原文内容
    content_html: Mapped[str | None] = mapped_column(Text)  # 渲染后的HTML内容
    summary: Mapped[str | None] = mapped_column(String(500))  # 文章摘要
    cover_image: Mapped[str | None] = mapped_column(String(500))  # 封面图片URL
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))  # 所属分类ID
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))  # 作者ID
    status: Mapped[str] = mapped_column(String(20), default="draft")  # 状态：draft/published
    is_top: Mapped[bool] = mapped_column(default=False)  # 是否置顶
    view_count: Mapped[int] = mapped_column(default=0)  # 浏览量
    like_count: Mapped[int] = mapped_column(default=0)  # 点赞数

    # 关联关系
    category: Mapped["Category | None"] = relationship(back_populates="articles")  # 所属分类
    author: Mapped["User"] = relationship(back_populates="articles")  # 作者
    tags: Mapped[list["Tag"]] = relationship(secondary="article_tags", back_populates="articles")  # 关联标签
    comments: Mapped[list["Comment"]] = relationship(back_populates="article", cascade="all, delete-orphan")  # 文章评论，级联删除
