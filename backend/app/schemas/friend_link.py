"""友情链接相关数据模式"""

from pydantic import BaseModel


class FriendLinkCreate(BaseModel):
    """友情链接创建请求模式"""

    title: str  # 链接标题
    url: str  # 链接地址
    logo: str | None = None  # Logo URL
    description: str | None = None  # 链接描述
    sort_order: int = 0  # 排序权重


class FriendLinkUpdate(BaseModel):
    """友情链接更新请求模式 - 所有字段可选"""

    title: str | None = None  # 链接标题
    url: str | None = None  # 链接地址
    logo: str | None = None  # Logo URL
    description: str | None = None  # 链接描述
    sort_order: int | None = None  # 排序权重


class FriendLinkOut(BaseModel):
    """友情链接输出模式"""

    id: int  # 链接ID
    title: str  # 链接标题
    url: str  # 链接地址
    logo: str | None  # Logo URL
    description: str | None  # 链接描述
    sort_order: int  # 排序权重

    model_config = {"from_attributes": True}  # 允许从ORM对象创建
