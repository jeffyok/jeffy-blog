"""用户管理数据模式 - 管理员更新用户、重置密码、分页查询"""

from pydantic import BaseModel, field_validator

from app.schemas.auth import UserOut


class UserUpdate(BaseModel):
    """管理员更新用户请求模式"""

    role: str | None = None       # 角色：user / admin
    is_active: bool | None = None  # 是否激活

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str | None) -> str | None:
        if v is not None and v not in ("user", "admin"):
            raise ValueError("角色必须是 user 或 admin")
        return v


class UserPasswordReset(BaseModel):
    """管理员重置用户密码请求模式"""

    new_password: str  # 新密码

    @field_validator("new_password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("密码长度不能少于6位")
        return v


class UserPaginationOut(BaseModel):
    """用户分页输出模式"""

    items: list[UserOut]  # 复用已有的用户输出模式
    total: int
    page: int
    page_size: int
