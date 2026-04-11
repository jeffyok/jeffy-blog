/**
 * 文章相关 API
 * 包含文章的 CRUD 操作
 */
import api from '.'
import type { Article, ArticleCreate, ArticlePagination, ArticleUpdate } from '@/types/article'

/** 获取文章列表（分页，支持分类/标签/搜索过滤） */
export function getArticles(params?: { page?: number; page_size?: number; category_id?: number; tag_id?: number; search?: string }) {
  return api.get<ArticlePagination>('/articles/', { params })
}

/** 根据 slug 获取文章详情 */
export function getArticle(slug: string) {
  return api.get<Article>(`/articles/${slug}`)
}

/** 创建新文章 */
export function createArticle(data: ArticleCreate) {
  return api.post<Article>('/articles/', data)
}

/** 更新文章 */
export function updateArticle(id: number, data: ArticleUpdate) {
  return api.put<Article>(`/articles/${id}`, data)
}

/** 删除文章 */
export function deleteArticle(id: number) {
  return api.delete(`/articles/${id}`)
}
