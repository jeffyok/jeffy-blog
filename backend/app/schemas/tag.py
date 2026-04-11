"""标签相关数据模式"""

from pydantic import BaseModel


class TagCreate(BaseModel):
    """标签创建请求模式"""

    name: str  # 标签名称
    slug: str | None = None  # URL标识，为空时自动生成


class TagUpdate(BaseModel):
    """标签更新请求模式 - 所有字段可选"""

    name: str | None = None  # 标签名称
    slug: str | None = None  # URL标识
