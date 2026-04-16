# -*- coding: utf-8 -*-
"""角色模型及角色-权限关联表"""

from datetime import datetime

from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.base import TimestampMixin


# 角色-权限多对多关联表
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", primary_key=True, comment="角色ID"),
    Column("permission_id", primary_key=True, comment="权限ID"),
    comment="角色-权限关联表",
)


# 用户-角色多对多关联表
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", primary_key=True, comment="用户ID"),
    Column("role_id", primary_key=True, comment="角色ID"),
    comment="用户-角色关联表",
)


class Role(Base, TimestampMixin):
    """角色模型 - RBAC 角色定义"""

    __tablename__ = "roles"
    __table_args__ = {"comment": "角色表"}

    id: Mapped[int] = mapped_column(primary_key=True, comment="主键ID")
    name: Mapped[str] = mapped_column(String(50), unique=True, comment="角色标识（如 super_admin, admin, editor）")
    display_name: Mapped[str] = mapped_column(String(50), comment="显示名称")
    description: Mapped[str | None] = mapped_column(String(200), comment="描述")
    is_default: Mapped[bool] = mapped_column(default=False, comment="是否为默认角色")

    # 关联关系：由于不使用数据库外键，改为在 Service 层手动查询
