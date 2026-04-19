/**
 * 评论相关 API
 * 包含前台评论获取/提交，后台评论管理
 */
import api from '.'
import type { Comment, CommentCreate } from '@/types/comment'

/** 获取文章评论列表 */
export function getComments(articleId: number) {
  return api.get<Comment[]>(`/articles/${articleId}/comments/`)
}

/** 发表评论（支持匿名） */
export function createComment(articleId: number, data: CommentCreate) {
  return api.post<Comment>(`/articles/${articleId}/comments/`, data)
}

/** 管理员获取评论列表（分页，支持状态过滤） */
export function adminGetComments(params?: { page?: number; page_size?: number; status?: string }) {
  return api.get('/admin/comments/', { params })
}

/** 更新评论状态（approved/rejected） */
export function updateCommentStatus(id: number, status: string) {
  return api.put(`/admin/comments/${id}?status=${status}`)
}

/** 删除评论 */
export function deleteComment(id: number) {
  return api.delete(`/admin/comments/${id}`)
}
