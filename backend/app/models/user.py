# -*- coding: utf-8 -*-
"""用户模型"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.base import TimestampMixin


class User(Base, TimestampMixin):
    """用户模型 - 存储用户账户信息"""

    __tablename__ = "users"
    __table_args__ = {"comment": "用户表"}

    id: Mapped[int] = mapped_column(primary_key=True, comment="主键ID")
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, comment="用户名")
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, comment="邮箱地址")
    password_hash: Mapped[str] = mapped_column(String(255), comment="密码哈希值")
    avatar: Mapped[str | None] = mapped_column(String(500), comment="头像URL")
    role: Mapped[str] = mapped_column(String(20), default="user", comment="角色：user-普通用户，admin-管理员")
    is_active: Mapped[bool] = mapped_column(default=True, comment="是否激活")

    # 关联关系
    articles: Mapped[list["Article"]] = relationship(back_populates="author")
    comments: Mapped[list["Comment"]] = relationship(back_populates="user")
