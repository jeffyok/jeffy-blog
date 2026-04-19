"""
管理端 - 用户管理 API 路由
用户列表查看、角色/状态编辑、密码重置、删除
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import UserOut
from app.schemas.user import UserPaginationOut, UserPasswordReset, UserUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/api/admin/users", tags=["admin-users"])


@router.get("/", response_model=UserPaginationOut)
async def get_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
    role: str | None = Query(None),
    is_active: bool | None = Query(None),
    db: AsyncSession = Depends(get_db),
    _=Depends(require_admin),
):
    """获取用户列表（分页、搜索、过滤），需管理员权限"""
    users, total = await UserService.get_users(db, page, page_size, search, role, is_active)
    return UserPaginationOut(items=users, total=total, page=page, page_size=page_size)


@router.put("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: int,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """更新用户角色/状态，需管理员权限"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")

    if user_id == current_user.id and data.is_active is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="不能禁用自己的账号")

    user = await UserService.update_user(db, user, data)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """删除用户，需管理员权限"""
    if user_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="不能删除自己的账号")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")

    await UserService.delete_user(db, user)


@router.put("/{user_id}/reset-password")
async def reset_password(
    user_id: int,
    data: UserPasswordReset,
    db: AsyncSession = Depends(get_db),
    _=Depends(require_admin),
):
    """重置用户密码，需管理员权限"""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")

    await UserService.reset_password(db, user, data.new_password)
    return {"message": "密码重置成功"}
