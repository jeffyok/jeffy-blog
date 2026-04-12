# -*- coding: utf-8 -*-
"""权限模型"""

from datetime import datetime, timezone

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Permission(Base):
    """权限模型 - RBAC 权限定义"""

    __tablename__ = "permissions"
    __table_args__ = {"comment": "权限表"}

    id: Mapped[int] = mapped_column(primary_key=True, comment="主键ID")
    name: Mapped[str] = mapped_column(String(100), unique=True, comment="权限标识（如 articles:create）")
    display_name: Mapped[str] = mapped_column(String(100), comment="显示名称")
    module: Mapped[str] = mapped_column(String(50), comment="所属模块（articles, categories, tags, comments, users）")
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc), comment="创建时间"
    )

    # 关联关系
    roles: Mapped[list["Role"]] = relationship(secondary="role_permissions", back_populates="permissions")
