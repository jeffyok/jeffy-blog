/**
 * 评论相关类型定义
 */

/** 评论用户简要信息 */
export interface CommentUser {
  id: number
  username: string
  avatar: string | null
}

/** 评论（含嵌套回复） */
export interface Comment {
  id: number
  content: string
  article_id: number
  user: CommentUser | null        // 登录用户
  nickname: string | null         // 匿名用户昵称
  parent_id: number | null        // 父评论 ID，null 表示顶级评论
  status: string
  created_at: string
  replies: Comment[]              // 子回复列表
}

/** 发表评论请求体 */
export interface CommentCreate {
  content: string
  parent_id?: number              // 回复某条评论时传入
  nickname?: string               // 匿名评论时必填
  email?: string                  // 匿名评论时必填
}
