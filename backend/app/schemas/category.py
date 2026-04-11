"""分类相关数据模式"""

from pydantic import BaseModel


class CategoryCreate(BaseModel):
    """分类创建请求模式"""

    name: str  # 分类名称
    slug: str | None = None  # URL标识，为空时自动生成
    description: str | None = None  # 分类描述


class CategoryUpdate(BaseModel):
    """分类更新请求模式 - 所有字段可选"""

    name: str | None = None  # 分类名称
    slug: str | None = None  # URL标识
    description: str | None = None  # 分类描述
