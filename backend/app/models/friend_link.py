"""友情链接模型"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class FriendLink(Base):
    """友情链接模型 - 博客友情链接管理"""

    __tablename__ = "friend_links"

    id: Mapped[int] = mapped_column(primary_key=True)  # 主键
    title: Mapped[str] = mapped_column(String(100))  # 链接标题
    url: Mapped[str] = mapped_column(String(500))  # 链接地址
    logo: Mapped[str | None] = mapped_column(String(500))  # 链接Logo URL
    description: Mapped[str | None] = mapped_column(String(200))  # 链接描述
    sort_order: Mapped[int] = mapped_column(default=0)  # 排序权重，值越小越靠前
