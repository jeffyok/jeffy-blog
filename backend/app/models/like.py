"""点赞模型"""

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Like(Base):
    """点赞模型 - 用户对文章的点赞记录（联合主键）"""

    __tablename__ = "likes"
    __table_args__ = {"comment": "文章点赞记录表"}

    user_id: Mapped[int] = mapped_column(primary_key=True, comment="用户ID")
    article_id: Mapped[int] = mapped_column(primary_key=True, comment="文章ID")
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, comment="点赞时间")

    # 关联关系
    article: Mapped["Article"] = relationship(foreign_keys=[article_id])
    user: Mapped["User"] = relationship(foreign_keys=[user_id])
