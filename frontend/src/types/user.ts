/**
 * 用户相关类型定义
 */
export interface User {
  id: number
  username: string
  email: string
  avatar: string | null
  role: 'admin' | 'user'
  is_active: boolean
  created_at: string
}

/** 用户分页响应 */
export interface UserPagination {
  items: User[]
  total: number
  page: number
  page_size: number
}

/** 管理员更新用户请求体 */
export interface UserUpdate {
  role?: 'admin' | 'user'
  is_active?: boolean
}

/** 管理员重置密码请求体 */
export interface UserPasswordReset {
  new_password: string
}
