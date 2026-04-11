"""标签模型及文章-标签关联表"""

from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Tag(Base):
    """标签模型 - 博客文章标签"""

    __tablename__ = "tags"
    __table_args__ = {"comment": "文章标签表"}

    id: Mapped[int] = mapped_column(primary_key=True, comment="主键ID")
    name: Mapped[str] = mapped_column(String(50), unique=True, comment="标签名称")
    slug: Mapped[str] = mapped_column(String(50), unique=True, index=True, comment="URL友好标识")

    articles: Mapped[list["Article"]] = relationship(
        secondary="article_tags",
        primaryjoin="Tag.id == article_tags.c.tag_id",
        secondaryjoin="Article.id == article_tags.c.article_id",
        back_populates="tags",
    )


# 文章与标签的多对多关联表
article_tags = Table(
    "article_tags",
    Base.metadata,
    Column("article_id", Integer, primary_key=True, comment="文章ID"),
    Column("tag_id", Integer, primary_key=True, comment="标签ID"),
    comment="文章与标签关联表",
)
