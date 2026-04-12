"""权限相关数据模式"""

from datetime import datetime

from pydantic import BaseModel


class PermissionOut(BaseModel):
    """权限输出模式"""

    id: int
    name: str
    display_name: str
    module: str
    created_at: datetime

    model_config = {"from_attributes": True}


class AssignRolesRequest(BaseModel):
    """分配用户角色请求"""

    role_ids: list[int]  # 角色ID列表
