/**
 * 标签相关 API
 * 包含标签的 CRUD 操作
 */
import api from '.'
import type { Tag as ArticleTag } from '@/types/article'
import type { TagCreate, TagUpdate } from '@/types/api'

/** 获取所有标签列表 */
export function getTags() {
  return api.get<ArticleTag[]>('/tags/')
}

/** 创建标签 */
export function createTag(data: TagCreate) {
  return api.post<ArticleTag>('/tags/', data)
}

/** 更新标签 */
export function updateTag(id: number, data: TagUpdate) {
  return api.put<ArticleTag>(`/tags/${id}`, data)
}

/** 删除标签 */
export function deleteTag(id: number) {
  return api.delete(`/tags/${id}`)
}
