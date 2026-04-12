/**
 * 文章列表状态管理
 * 缓存文章列表数据，避免重复请求
 */
import { ref } from 'vue'
import { defineStore } from 'pinia'
import type { ArticleListItem, ArticlePagination } from '@/types/article'
import * as articlesApi from '@/api/articles'

export const useArticlesStore = defineStore('articles', () => {
  const articles = ref<ArticleListItem[]>([])
  const total = ref(0)
  const loading = ref(false)

  /** 获取文章列表（分页，支持过滤） */
  async function fetchArticles(params?: { page?: number; page_size?: number; category_id?: number; tag_id?: number; search?: string; status?: string }) {
    loading.value = true
    try {
      const { data } = await articlesApi.getArticles(params)
      articles.value = data.items
      total.value = data.total
    } finally {
      loading.value = false
    }
  }

  return { articles, total, loading, fetchArticles }
})
