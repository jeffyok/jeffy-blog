"""
权限管理 API 路由（只读）
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_permission
from app.db.session import get_db
from app.models.user import User
from app.schemas.permission import PermissionOut
from app.services.rbac_service import RBACService

router = APIRouter(prefix="/api/permissions", tags=["permissions"])


@router.get("", response_model=list[PermissionOut])
async def list_permissions(
    module: str | None = Query(None, description="按模块筛选"),
    current_user: User = Depends(require_permission("users:view")),
    db: AsyncSession = Depends(get_db),
):
    """获取所有权限"""
    return await RBACService.get_all_permissions(db, module=module)
