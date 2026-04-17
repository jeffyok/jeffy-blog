from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_admin
from app.db.session import get_db
from app.models.comment import Comment
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentOut
from app.services.comment_service import CommentService

router = APIRouter(prefix="/api", tags=["comments"])


@router.get("/articles/{article_id}/comments")
async def get_comments(article_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await CommentService.get_comments_with_user_info(db, article_id)
    except Exception as e:
        import traceback
        print(f"Error getting comments: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/articles/{article_id}/comments", status_code=201)
async def create_comment(
    article_id: int,
    data: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User | None = Depends(get_current_user),
):
    # Guest comments must have nickname and email
    if current_user is None and (not data.nickname or not data.email):
        raise HTTPException(status_code=400, detail="Guest comments require nickname and email")
    comment = await CommentService.create_comment(db, article_id, data, user_id=current_user.id if current_user else None)
    # 返回组装后的评论数据
    comments = await CommentService.get_comments_with_user_info(db, article_id)
    # 找到刚创建的评论
    for c in comments:
        if c["id"] == comment.id:
            # 转换 user 字段，只保留必要的信息
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
    # 如果没找到（比如评论状态不是 approved），返回基本的评论数据
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


# Admin endpoints
@router.get("/admin/comments")
async def list_comments(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: str | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    comments, total = await CommentService.get_all_comments_with_user_info(db, page=page, page_size=page_size, status=status)
    return {"items": comments, "total": total, "page": page, "page_size": page_size}


@router.put("/admin/comments/{comment_id}")
async def update_comment_status(
    comment_id: int,
    status: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    comment = await CommentService.update_comment_status(db, comment_id, status)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    # 返回组装后的评论数据
    comments, _ = await CommentService.get_comments_with_user_info(db, comment.article_id)
    for c in comments:
        if c["id"] == comment.id:
            return c
    return {"id": comment.id, "content": comment.content, "article_id": comment.article_id, "user_id": comment.user_id, "nickname": comment.nickname, "parent_id": comment.parent_id, "status": comment.status, "created_at": comment.created_at}


@router.delete("/admin/comments/{comment_id}", status_code=204)
async def delete_comment(comment_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)):
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    await CommentService.delete_comment(db, comment)
