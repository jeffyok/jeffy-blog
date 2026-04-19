"""
C 端 - 评论 API 路由
获取评论列表和发表评论（支持匿名评论）
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_optional_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.comment import CommentCreate
from app.services.comment_service import CommentService

router = APIRouter(prefix="/api", tags=["comments"])


@router.get("/articles/{article_id}/comments/")
async def get_comments(article_id: int, db: AsyncSession = Depends(get_db)):
    """获取文章评论列表"""
    try:
        return await CommentService.get_comments_with_user_info(db, article_id)
    except Exception as e:
        import traceback
        print(f"Error getting comments: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/articles/{article_id}/comments/", status_code=201)
async def create_comment(
    article_id: int,
    data: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User | None = Depends(get_optional_current_user),
):
    """发表评论（登录用户或游客均可，游客需填写昵称和邮箱）"""
    if current_user is None and (not data.nickname or not data.email):
        raise HTTPException(status_code=400, detail="Guest comments require nickname and email")
    comment = await CommentService.create_comment(db, article_id, data, user_id=current_user.id if current_user else None)
    # 返回组装后的评论数据
    comments = await CommentService.get_comments_with_user_info(db, article_id)
    for c in comments:
        if c["id"] == comment.id:
            result = {
                "id": c["id"],
                "content": c["content"],
                "article_id": c["article_id"],
                "user": None,
                "nickname": c["nickname"],
                "parent_id": c["parent_id"],
                "status": c["status"],
                "created_at": c["created_at"]
            }
            if c["user"]:
                result["user"] = {
                    "id": c["user"]["id"],
                    "username": c["user"]["username"],
                    "avatar": c["user"]["avatar"]
                }
            return result
    return {
        "id": comment.id,
        "content": comment.content,
        "article_id": comment.article_id,
        "user": None,
        "nickname": comment.nickname,
        "parent_id": comment.parent_id,
        "status": comment.status,
        "created_at": comment.created_at
    }
