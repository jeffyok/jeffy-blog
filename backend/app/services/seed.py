"""
RBAC 种子数据 - 初始化预置角色和权限

使用方式：cd backend && python -m app.services.seed
"""

# 导入所有模型以确保 SQLAlchemy registry 注册
from app.models import user, article, category, tag, comment, like, friend_link  # noqa: F401

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.models.permission import Permission
from app.models.role import Role, role_permissions, user_roles
from app.models.user import User

# 预置权限定义
PERMISSIONS = [
    ("articles:view", "查看文章", "articles"),
    ("articles:create", "创建文章", "articles"),
    ("articles:edit", "编辑文章", "articles"),
    ("articles:delete", "删除文章", "articles"),
    ("categories:view", "查看分类", "categories"),
    ("categories:create", "创建分类", "categories"),
    ("categories:edit", "编辑分类", "categories"),
    ("categories:delete", "删除分类", "categories"),
    ("tags:view", "查看标签", "tags"),
    ("tags:create", "创建标签", "tags"),
    ("tags:edit", "编辑标签", "tags"),
    ("tags:delete", "删除标签", "tags"),
    ("comments:view", "查看评论", "comments"),
    ("comments:approve", "审核评论", "comments"),
    ("comments:delete", "删除评论", "comments"),
    ("users:view", "查看用户", "users"),
    ("users:edit", "编辑用户", "users"),
    ("users:delete", "删除用户", "users"),
    ("friends:view", "查看友链", "friends"),
    ("friends:create", "创建友链", "friends"),
    ("friends:edit", "编辑友链", "friends"),
    ("friends:delete", "删除友链", "friends"),
    ("dashboard:view", "查看仪表盘", "dashboard"),
]

# 预置角色定义：(name, display_name, description, is_default, [permission_names])
ROLES = [
    ("super_admin", "超级管理员", "拥有所有权限", False, "*"),
    ("admin", "管理员", "除用户管理外的所有权限", False, [
        "articles:view", "articles:create", "articles:edit", "articles:delete",
        "categories:view", "categories:create", "categories:edit", "categories:delete",
        "tags:view", "tags:create", "tags:edit", "tags:delete",
        "comments:view", "comments:approve", "comments:delete",
        "friends:view", "friends:create", "friends:edit", "friends:delete",
        "dashboard:view",
    ]),
    ("editor", "编辑者", "文章、分类、标签管理", False, [
        "articles:view", "articles:create", "articles:edit",
        "categories:view", "categories:create", "categories:edit",
        "tags:view", "tags:create", "tags:edit",
        "dashboard:view",
    ]),
    ("user", "普通用户", "默认角色，无后台权限", True, []),
]


async def seed_permissions(db: AsyncSession) -> dict[str, Permission]:
    """初始化权限数据"""
    perm_map: dict[str, Permission] = {}
    for name, display_name, module in PERMISSIONS:
        result = await db.execute(select(Permission).where(Permission.name == name))
        perm = result.scalar_one_or_none()
        if not perm:
            perm = Permission(name=name, display_name=display_name, module=module)
            db.add(perm)
            await db.flush()
        perm_map[name] = perm
    return perm_map


async def seed_roles(db: AsyncSession, perm_map: dict[str, Permission]) -> dict[str, int]:
    """初始化角色数据并分配权限"""
    role_map: dict[str, int] = {}
    for name, display_name, description, is_default, perm_names in ROLES:
        result = await db.execute(select(Role).where(Role.name == name))
        role = result.scalar_one_or_none()
        if not role:
            role = Role(name=name, display_name=display_name, description=description, is_default=is_default)
            db.add(role)
            await db.flush()
        role_map[name] = role.id

        # 通过直接插入关联表来分配权限
        perm_ids = []
        if perm_names == "*":
            perm_ids = [p.id for p in perm_map.values()]
        else:
            perm_ids = [perm_map[pn].id for pn in perm_names if pn in perm_map]

        # 先清除旧权限，再重新分配
        await db.execute(delete(role_permissions).where(role_permissions.c.role_id == role.id))
        for pid in perm_ids:
            await db.execute(role_permissions.insert().values(role_id=role.id, permission_id=pid))

    return role_map


async def migrate_existing_admin(db: AsyncSession, role_map: dict[str, int]) -> None:
    """将现有 admin 用户迁移到超级管理员角色"""
    super_admin_id = role_map.get("super_admin")
    if not super_admin_id:
        return
    result = await db.execute(select(User).where(User.role == "admin"))
    admins = result.scalars().all()
    for admin_user in admins:
        # 检查是否已有该角色
        existing = await db.execute(
            select(user_roles).where(
                user_roles.c.user_id == admin_user.id,
                user_roles.c.role_id == super_admin_id,
            )
        )
        if existing.scalar_one_or_none() is None:
            await db.execute(
                user_roles.insert().values(user_id=admin_user.id, role_id=super_admin_id)
            )


async def run_seed():
    """执行种子数据初始化"""
    async with AsyncSessionLocal() as db:
        perm_map = await seed_permissions(db)
        role_map = await seed_roles(db, perm_map)
        await migrate_existing_admin(db, role_map)
        await db.commit()
        print("RBAC 种子数据初始化完成")
        print(f"  权限: {len(perm_map)} 条")
        print(f"  角色: {len(role_map)} 条")


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_seed())
