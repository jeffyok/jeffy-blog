"""分类模型"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Category(Base):
    """分类模型 - 博客文章分类"""

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)  # 主键
    name: Mapped[str] = mapped_column(String(50), unique=True)  # 分类名称，唯一
    slug: Mapped[str] = mapped_column(String(50), unique=True, index=True)  # URL友好标识，唯一且建索引
    description: Mapped[str | None] = mapped_column(String(200))  # 分类描述

    articles: Mapped[list["Article"]] = relationship(back_populates="category")  # 该分类下的文章
