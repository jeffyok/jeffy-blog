"""点赞模型"""

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Like(Base):
    """点赞模型 - 用户对文章的点赞记录（联合主键）"""

    __tablename__ = "likes"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)  # 用户ID，联合主键
    article_id: Mapped[int] = mapped_column(ForeignKey("articles.id", ondelete="CASCADE"), primary_key=True)  # 文章ID，联合主键
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)  # 点赞时间
