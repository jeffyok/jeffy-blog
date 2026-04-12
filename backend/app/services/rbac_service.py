"""RBAC 管理服务 - 角色、权限的业务逻辑"""

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.permission import Permission
from app.models.role import Role, role_permissions
from app.models.user import User


class RBACService:
    """RBAC 管理服务"""

    @staticmethod
    async def get_all_roles(db: AsyncSession) -> list[Role]:
        """获取所有角色"""
        result = await db.execute(select(Role).options(selectinload(Role.permissions)).order_by(Role.id))
        return list(result.scalars().all())

    @staticmethod
    async def get_role_by_id(db: AsyncSession, role_id: int) -> Role | None:
        """根据ID获取角色"""
        result = await db.execute(
            select(Role).options(selectinload(Role.permissions)).where(Role.id == role_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_role_by_name(db: AsyncSession, name: str) -> Role | None:
        """根据名称获取角色"""
        result = await db.execute(select(Role).where(Role.name == name))
        return result.scalar_one_or_none()

    @staticmethod
    async def create_role(db: AsyncSession, name: str, display_name: str, description: str | None = None,
                          permission_ids: list[int] | None = None) -> Role:
        """创建角色"""
        existing = await RBACService.get_role_by_name(db, name)
        if existing:
            raise HTTPException(status_code=400, detail="Role already exists")
        role = Role(name=name, display_name=display_name, description=description)
        if permission_ids:
            perms = await db.execute(select(Permission).where(Permission.id.in_(permission_ids)))
            role.permissions = list(perms.scalars().all())
        db.add(role)
        await db.commit()
        await db.refresh(role, ["permissions"])
        return role

    @staticmethod
    async def update_role(db: AsyncSession, role_id: int, display_name: str | None = None,
                          description: str | None = None, permission_ids: list[int] | None = None) -> Role:
        """更新角色"""
        role = await RBACService.get_role_by_id(db, role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        if display_name is not None:
            role.display_name = display_name
        if description is not None:
            role.description = description
        if permission_ids is not None:
            perms = await db.execute(select(Permission).where(Permission.id.in_(permission_ids)))
            role.permissions = list(perms.scalars().all())
        await db.commit()
        await db.refresh(role, ["permissions"])
        return role

    @staticmethod
    async def delete_role(db: AsyncSession, role_id: int) -> None:
        """删除角色"""
        role = await RBACService.get_role_by_id(db, role_id)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        await db.delete(role)
        await db.commit()

    @staticmethod
    async def get_all_permissions(db: AsyncSession, module: str | None = None) -> list[Permission]:
        """获取所有权限，可按模块筛选"""
        query = select(Permission).order_by(Permission.module, Permission.id)
        if module:
            query = query.where(Permission.module == module)
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def assign_roles_to_user(db: AsyncSession, user_id: int, role_ids: list[int]) -> User:
        """为用户分配角色"""
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        roles = await db.execute(select(Role).where(Role.id.in_(role_ids)))
        user.roles = list(roles.scalars().all())
        await db.commit()
        await db.refresh(user, ["roles"])
        return user

    @staticmethod
    async def get_user_permissions(db: AsyncSession, user_id: int) -> list[str]:
        """获取用户的所有权限名称"""
        from app.models.user import User
        from app.models.role import Role, user_roles
        result = await db.execute(
            select(Permission.name)
            .join(role_permissions, Permission.id == role_permissions.c.permission_id)
            .join(Role, role_permissions.c.role_id == Role.id)
            .join(user_roles, Role.id == user_roles.c.role_id)
            .where(user_roles.c.user_id == user_id)
        )
        return [row[0] for row in result.all()]
