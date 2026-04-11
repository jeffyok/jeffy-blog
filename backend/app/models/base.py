"""模型基础模块 - 提供时间戳混入类"""

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class TimestampMixin:
    """时间戳混入类 - 为模型自动添加创建时间和更新时间"""

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
