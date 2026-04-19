"""用户管理服务 - 处理管理员对用户的查询、更新、删除和密码重置"""

from fastapi import HTTPException, status
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserUpdate


class UserService:
    """用户管理服务类 - 封装管理员操作用户的业务逻辑"""

    @staticmethod
    async def get_users(
        db: AsyncSession,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
        role: str | None = None,
        is_active: bool | None = None,
    ) -> tuple[list[User], int]:
        """分页查询用户列表，支持搜索和过滤"""
        query = select(User)
        count_query = select(func.count(User.id))

        # 搜索条件：按用户名或邮箱模糊匹配
        if search:
            search_filter = or_(
                User.username.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%"),
            )
            query = query.where(search_filter)
            count_query = count_query.where(search_filter)

        # 角色过滤
        if role:
            query = query.where(User.role == role)
            count_query = count_query.where(User.role == role)

        # 状态过滤
        if is_active is not None:
            query = query.where(User.is_active == is_active)
            count_query = count_query.where(User.is_active == is_active)

        # 获取总数
        total = (await db.execute(count_query)).scalar() or 0

        # 按创建时间降序排序并分页
        query = query.order_by(User.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
        result = await db.execute(query)
        users = list(result.scalars().all())

        return users, total

    @staticmethod
    async def update_user(db: AsyncSession, user: User, data: UserUpdate) -> User:
        """更新用户角色/状态，仅更新非 None 字段"""
        # 最后管理员保护：如果将管理员降级为普通用户，检查是否是最后一个管理员
        if data.role == "user" and user.role == "admin":
            admin_count = (await db.execute(
                select(func.count(User.id)).where(User.role == "admin")
            )).scalar() or 0
            if admin_count <= 1:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="不能降级最后一个管理员",
                )

        if data.role is not None:
            user.role = data.role
        if data.is_active is not None:
            user.is_active = data.is_active

        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def delete_user(db: AsyncSession, user: User) -> None:
        """删除用户"""
        await db.delete(user)
        await db.commit()

    @staticmethod
    async def reset_password(db: AsyncSession, user: User, new_password: str) -> None:
        """重置用户密码"""
        user.password_hash = hash_password(new_password)
        await db.commit()
