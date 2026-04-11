/**
 * 管理后台 API
 * 包含仪表盘统计和归档数据
 */
import api from '.'
import type { DashboardStats } from '@/types/api'
import type { ArchiveYear } from '@/types/api'

/** 获取后台仪表盘统计数据 */
export function getDashboardStats() {
  return api.get<DashboardStats>('/admin/dashboard')
}

/** 获取文章归档数据（按年月分组） */
export function getArchives() {
  return api.get<{ archives: ArchiveYear[] }>('/archives')
}
