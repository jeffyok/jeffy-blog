/**
 * 管理后台 API
 * 包含仪表盘统计、归档数据和用户管理
 */
import api from '.'
import type { DashboardStats } from '@/types/api'
import type { ArchiveYear } from '@/types/api'
import type { UserPagination, UserUpdate, UserPasswordReset } from '@/types/user'

/** 获取后台仪表盘统计数据 */
export function getDashboardStats() {
  return api.get<DashboardStats>('/admin/dashboard')
}

/** 获取文章归档数据（按年月分组） */
export function getArchives() {
  return api.get<{ archives: ArchiveYear[] }>('/archives')
}

// ==================== 用户管理 ====================

/** 获取用户列表（分页，支持搜索和过滤） */
export function adminGetUsers(params?: {
  page?: number
  page_size?: number
  search?: string
  role?: string
  is_active?: boolean
}) {
  return api.get<UserPagination>('/admin/users', { params })
}

/** 更新用户角色/状态 */
export function adminUpdateUser(id: number, data: UserUpdate) {
  return api.put(`/admin/users/${id}`, data)
}

/** 删除用户 */
export function adminDeleteUser(id: number) {
  return api.delete(`/admin/users/${id}`)
}

/** 重置用户密码 */
export function adminResetPassword(id: number, data: UserPasswordReset) {
  return api.put(`/admin/users/${id}/reset-password`, data)
}
