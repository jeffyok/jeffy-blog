"""评论相关数据模式"""

from datetime import datetime

from pydantic import BaseModel


class CommentCreate(BaseModel):
    """评论创建请求模式"""

    content: str  # 评论内容
    parent_id: int | None = None  # 父评论ID，用于回复
    nickname: str | None = None  # 游客昵称
    email: str | None = None  # 游客邮箱


class CommentUserOut(BaseModel):
    """评论中的用户信息输出模式"""

    id: int  # 用户ID
    username: str  # 用户名
    avatar: str | None = None  # 头像URL

    model_config = {"from_attributes": True}  # 允许从ORM对象创建


class CommentOut(BaseModel):
    """评论输出模式"""

    id: int  # 评论ID
    content: str  # 评论内容
    article_id: int  # 所属文章ID
    user: CommentUserOut | None = None  # 评论者信息（登录用户）
    nickname: str | None = None  # 游客昵称
    parent_id: int | None = None  # 父评论ID
    status: str  # 评论状态
    created_at: datetime  # 创建时间

    model_config = {"from_attributes": True}  # 允许从ORM对象创建
