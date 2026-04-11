"""认证相关数据模式 - 用户注册、登录及令牌校验"""

from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """用户注册请求模式"""

    username: str  # 用户名
    email: EmailStr  # 邮箱
    password: str  # 密码


class UserLogin(BaseModel):
    """用户登录请求模式"""

    username: str  # 用户名
    password: str  # 密码


class Token(BaseModel):
    """JWT令牌响应模式"""

    access_token: str  # 访问令牌
    token_type: str = "bearer"  # 令牌类型


class UserOut(BaseModel):
    """用户信息输出模式"""

    id: int  # 用户ID
    username: str  # 用户名
    email: str  # 邮箱
    avatar: str | None = None  # 头像URL
    role: str  # 角色
    is_active: bool  # 是否激活
    created_at: datetime  # 创建时间

    model_config = {"from_attributes": True}  # 允许从ORM对象创建
