/**
 * 认证相关 API
 * 包含注册、登录、获取当前用户信息
 */
import api from '.'
import type { User } from '@/types/user'

/** 用户注册 */
export function register(username: string, email: string, password: string) {
  return api.post<User>('/auth/register', { username, email, password })
}

/** 用户登录，使用 form-data 格式提交 */
export function login(username: string, password: string) {
  const formData = new URLSearchParams()
  formData.append('username', username)
  formData.append('password', password)
  return api.post<{ access_token: string; token_type: string }>('/auth/login', formData)
}

/** 获取当前登录用户信息 */
export function getMe() {
  return api.get<User>('/auth/me')
}
