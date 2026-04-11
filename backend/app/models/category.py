"""分类模型"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Category(Base):
    """分类模型 - 博客文章分类"""

    __tablename__ = "categories"
    __table_args__ = {"comment": "文章分类表"}

    id: Mapped[int] = mapped_column(primary_key=True, comment="主键ID")
    name: Mapped[str] = mapped_column(String(50), unique=True, comment="分类名称")
    slug: Mapped[str] = mapped_column(String(50), unique=True, index=True, comment="URL友好标识")
    description: Mapped[str | None] = mapped_column(String(200), comment="分类描述")

    articles: Mapped[list["Article"]] = relationship(back_populates="category")
