"""用户模型"""

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from app.db.session import Base
from app.models.base import TimestampMixin


class User(Base, TimestampMixin):
    """用户模型 - 存储用户账户信息"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)  # 主键
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)  # 用户名，唯一且建索引
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)  # 邮箱，唯一且建索引
    password_hash: Mapped[str] = mapped_column(String(255))  # 密码哈希值
    avatar: Mapped[str | None] = mapped_column(String(500))  # 头像URL
    role: Mapped[str] = mapped_column(String(20), default="user")  # 角色：user/admin
    is_active: Mapped[bool] = mapped_column(default=True)  # 是否激活
