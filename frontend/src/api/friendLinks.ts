/**
 * 友情链接 API
 * 前台获取列表，后台管理
 */
import api from '.'
import type { FriendLink, FriendLinkCreate, FriendLinkUpdate } from '@/types/api'

/** 获取友情链接列表（前台） */
export function getFriendLinks() {
  return api.get<FriendLink[]>('/friend-links')
}

/** 创建友情链接（后台） */
export function createFriendLink(data: FriendLinkCreate) {
  return api.post<FriendLink>('/admin/friend-links', data)
}

/** 更新友情链接（后台） */
export function updateFriendLink(id: number, data: FriendLinkUpdate) {
  return api.put<FriendLink>(`/admin/friend-links/${id}`, data)
}

/** 删除友情链接（后台） */
export function deleteFriendLink(id: number) {
  return api.delete(`/admin/friend-links/${id}`)
}
