"""角色相关数据模式"""

from datetime import datetime

from pydantic import BaseModel


class RoleCreate(BaseModel):
    """创建角色请求"""

    name: str  # 角色标识
    display_name: str  # 显示名称
    description: str | None = None  # 描述
    permission_ids: list[int] = []  # 权限ID列表


class RoleUpdate(BaseModel):
    """更新角色请求"""

    display_name: str | None = None  # 显示名称
    description: str | None = None  # 描述
    permission_ids: list[int] | None = None  # 权限ID列表


class RoleOut(BaseModel):
    """角色输出模式"""

    id: int
    name: str
    display_name: str
    description: str | None = None
    is_default: bool = False
    created_at: datetime

    model_config = {"from_attributes": True}


class RoleWithPermissions(RoleOut):
    """角色及其权限输出"""

    permission_ids: list[int] = []
