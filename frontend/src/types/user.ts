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
