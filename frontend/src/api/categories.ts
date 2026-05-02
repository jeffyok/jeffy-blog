/**
 * 分类相关 API
 * 包含分类的 CRUD 操作
 */
import api from '.'
import type { CategoryCreate, CategoryUpdate } from '@/types/api'
import type { Category as ArticleCategory } from '@/types/article'

/** 获取所有分类列表 */
export function getCategories() {
  return api.get<ArticleCategory[]>('/categories/')
}

/** 管理后台获取所有分类列表 */
export function adminGetCategories() {
  return api.get<ArticleCategory[]>('/admin/categories/')
}

/** 创建分类 */
export function createCategory(data: CategoryCreate) {
  return api.post<ArticleCategory>('/admin/categories/', data)
}

/** 更新分类 */
export function updateCategory(id: number, data: CategoryUpdate) {
  return api.put<ArticleCategory>(`/admin/categories/${id}`, data)
}

/** 删除分类 */
export function deleteCategory(id: number) {
  return api.delete(`/admin/categories/${id}`)
}
