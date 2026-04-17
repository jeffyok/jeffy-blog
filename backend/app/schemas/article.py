"""文章相关数据模式"""

from datetime import datetime

from pydantic import BaseModel


class ArticleCreate(BaseModel):
    """文章创建请求模式"""

    title: str  # 文章标题
    slug: str | None = None  # URL标识，为空时自动生成
    content: str  # Markdown内容
    summary: str | None = None  # 摘要，为空时自动提取
    cover_image: str | None = None  # 封面图片URL
    category_id: int | None = None  # 分类ID
    tag_ids: list[int] = []  # 标签ID列表
    status: str = "draft"  # 状态：draft/published
    is_top: bool = False  # 是否置顶


class ArticleUpdate(BaseModel):
    """文章更新请求模式 - 所有字段可选"""

    title: str | None = None  # 文章标题
    slug: str | None = None  # URL标识
    content: str | None = None  # Markdown内容
    summary: str | None = None  # 摘要
    cover_image: str | None = None  # 封面图片URL
    category_id: int | None = None  # 分类ID
    tag_ids: list[int] | None = None  # 标签ID列表
    status: str | None = None  # 状态
    is_top: bool | None = None  # 是否置顶


class TagOut(BaseModel):
    """标签输出模式"""

    id: int  # 标签ID
    name: str  # 标签名称
    slug: str  # URL标识
    created_at: datetime  # 创建时间

    model_config = {"from_attributes": True}  # 允许从ORM对象创建


class CategoryOut(BaseModel):
    """分类输出模式"""

    id: int  # 分类ID
    name: str  # 分类名称
    slug: str  # URL标识
    description: str | None = None  # 分类描述
    created_at: datetime  # 创建时间

    model_config = {"from_attributes": True}  # 允许从ORM对象创建


class AuthorOut(BaseModel):
    """作者信息输出模式"""

    id: int  # 作者ID
    username: str  # 用户名
    avatar: str | None = None  # 头像URL

    model_config = {"from_attributes": True}  # 允许从ORM对象创建


class ArticleListOut(BaseModel):
    """文章列表输出模式 - 不包含正文内容"""

    id: int  # 文章ID
    title: str  # 标题
    slug: str  # URL标识
    summary: str | None  # 摘要
    cover_image: str | None  # 封面图片
    category: CategoryOut | None  # 所属分类
    tags: list[TagOut]  # 关联标签列表
    author: AuthorOut  # 作者信息
    status: str  # 状态
    is_top: bool  # 是否置顶
    view_count: int  # 浏览量
    like_count: int  # 点赞数
    created_at: datetime  # 创建时间
    updated_at: datetime  # 更新时间

    model_config = {"from_attributes": True}  # 允许从ORM对象创建


class ArticleOut(ArticleListOut):
    """文章详情输出模式 - 继承列表模式，额外包含正文"""

    content: str  # Markdown正文
    content_html: str | None  # 渲染后的HTML正文


class ArticlePaginationOut(BaseModel):
    """文章分页输出模式"""

    items: list[ArticleListOut]  # 文章列表
    total: int  # 总数
    page: int  # 当前页码
    page_size: int  # 每页数量
