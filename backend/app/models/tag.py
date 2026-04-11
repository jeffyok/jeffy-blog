"""标签模型及文章-标签关联表"""

from sqlalchemy import ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Tag(Base):
    """标签模型 - 博客文章标签"""

    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)  # 主键
    name: Mapped[str] = mapped_column(String(50), unique=True)  # 标签名称，唯一
    slug: Mapped[str] = mapped_column(String(50), unique=True, index=True)  # URL友好标识，唯一且建索引

    articles: Mapped[list["Article"]] = relationship(secondary="article_tags", back_populates="tags")  # 关联文章


# 文章与标签的多对多关联表
article_tags = Table(
    "article_tags",
    Base.metadata,
    mapped_column("article_id", ForeignKey("articles.id", ondelete="CASCADE"), primary_key=True),  # 文章ID
    mapped_column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),  # 标签ID
)
