"""
管理端 - 评论管理 API 路由
评论列表查看、状态审核、删除（需管理员权限）
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_admin
from app.db.session import get_db
from app.models.comment import Comment
from app.models.user import User
from app.services.comment_service import CommentService

router = APIRouter(prefix="/api/admin/comments", tags=["admin-comments"])


@router.get("/")
async def list_comments(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: str | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """获取评论管理列表（分页，支持状态过滤）"""
    comments, total = await CommentService.get_all_comments_with_user_info(db, page=page, page_size=page_size, status=status)
    return {"items": comments, "total": total, "page": page, "page_size": page_size}


@router.put("/{comment_id}")
async def update_comment_status(
    comment_id: int,
    status: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """更新评论状态（需管理员权限）"""
    comment = await CommentService.update_comment_status(db, comment_id, status)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    comments, _ = await CommentService.get_comments_with_user_info(db, comment.article_id)
    for c in comments:
        if c["id"] == comment.id:
            return c
    return {"id": comment.id, "content": comment.content, "article_id": comment.article_id, "user_id": comment.user_id, "nickname": comment.nickname, "parent_id": comment.parent_id, "status": comment.status, "created_at": comment.created_at}


@router.delete("/{comment_id}", status_code=204)
async def delete_comment(comment_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_admin)):
    """删除评论（需管理员权限）"""
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    comment = result.scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    await CommentService.delete_comment(db, comment)
