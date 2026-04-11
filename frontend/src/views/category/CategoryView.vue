<!-- 分类页面：根据分类 slug 展示该分类下的文章列表 -->
<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getArticles } from '@/api/articles'
import { getCategories } from '@/api/categories'
import type { ArticleListItem, Category } from '@/types/article'
import ArticleCard from '@/components/article/ArticleCard.vue'
import Pagination from '@/components/common/Pagination.vue'

const route = useRoute()
const articles = ref<ArticleListItem[]>([])
const total = ref(0)
const loading = ref(true)
const page = ref(1)
const category = ref<Category | null>(null)
const pageSize = 10

/** 加载分类信息并拉取该分类下的文章 */
async function loadCategory() {
  loading.value = true
  try {
    // 从全部分类中找到当前 slug 对应的分类
    const catRes = await getCategories()
    category.value = catRes.data.find((c) => c.slug === route.params.slug) || null
    await loadArticles()
  } finally {
    loading.value = false
  }
}

/** 根据分类 ID 加载文章列表 */
async function loadArticles() {
  const { data } = await getArticles({ page: page.value, page_size: pageSize, category_id: category.value?.id })
  articles.value = data.items
  total.value = data.total
}

onMounted(loadCategory)
watch(() => route.params.slug, loadCategory)  // slug 变化时重新加载
watch(page, loadArticles)                     // 页码变化时重新加载
</script>

<template>
  <div>
    <h1 class="page-title">Category: {{ category?.name || route.params.slug }}</h1>
    <div v-if="loading" class="loading"><span>Loading...</span></div>
    <div v-else-if="articles.length === 0" class="empty">No articles in this category.</div>
    <template v-else>
      <ArticleCard v-for="article in articles" :key="article.id" :article="article" />
      <Pagination :total="total" :page="page" :page-size="pageSize" @update:page="page = $event" />
    </template>
  </div>
</template>
