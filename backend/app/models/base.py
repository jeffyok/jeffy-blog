# -*- coding: utf-8 -*-
"""模型基础模块 - 提供时间戳混入类"""

from datetime import datetime, timezone

from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class TimestampMixin:
    """时间戳混入类 - 为模型自动添加创建时间和更新时间（使用UTC时区）"""

    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc), comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        comment="更新时间",
    )
