"""
角色管理 API 路由
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_permission, require_role
from app.db.session import get_db
from app.models.user import User
from app.schemas.permission import AssignRolesRequest
from app.schemas.role import RoleCreate, RoleOut, RoleUpdate, RoleWithPermissions
from app.services.rbac_service import RBACService

router = APIRouter(prefix="/api/roles", tags=["roles"])


@router.get("", response_model=list[RoleWithPermissions])
async def list_roles(
    current_user: User = Depends(require_permission("users:view")),
    db: AsyncSession = Depends(get_db),
):
    """获取所有角色（含权限）"""
    return await RBACService.get_all_roles(db)


@router.post("", response_model=RoleWithPermissions, status_code=201)
async def create_role(
    role_data: RoleCreate,
    current_user: User = Depends(require_permission("users:create")),
    db: AsyncSession = Depends(get_db),
):
    """创建角色"""
    return await RBACService.create_role(
        db,
        name=role_data.name,
        display_name=role_data.display_name,
        description=role_data.description,
        permission_ids=role_data.permission_ids,
    )


@router.get("/{role_id}", response_model=RoleWithPermissions)
async def get_role(
    role_id: int,
    current_user: User = Depends(require_permission("users:view")),
    db: AsyncSession = Depends(get_db),
):
    """获取角色详情"""
    role = await RBACService.get_role_by_id(db, role_id)
    if not role:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.put("/{role_id}", response_model=RoleWithPermissions)
async def update_role(
    role_id: int,
    role_data: RoleUpdate,
    current_user: User = Depends(require_permission("users:edit")),
    db: AsyncSession = Depends(get_db),
):
    """更新角色"""
    return await RBACService.update_role(
        db, role_id,
        display_name=role_data.display_name,
        description=role_data.description,
        permission_ids=role_data.permission_ids,
    )


@router.delete("/{role_id}", status_code=204)
async def delete_role(
    role_id: int,
    current_user: User = Depends(require_permission("users:delete")),
    db: AsyncSession = Depends(get_db),
):
    """删除角色"""
    await RBACService.delete_role(db, role_id)


@router.post("/users/{user_id}/assign", status_code=200)
async def assign_roles(
    user_id: int,
    data: AssignRolesRequest,
    current_user: User = Depends(require_permission("users:edit")),
    db: AsyncSession = Depends(get_db),
):
    """为用户分配角色"""
    user = await RBACService.assign_roles_to_user(db, user_id, data.role_ids)
    return {"message": "Roles assigned successfully"}
