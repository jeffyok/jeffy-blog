<!-- 搜索页面：根据关键词搜索文章 -->
<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getArticles } from '@/api/articles'
import type { ArticleListItem } from '@/types/article'
import ArticleCard from '@/components/article/ArticleCard.vue'

const route = useRoute()
const router = useRouter()
const articles = ref<ArticleListItem[]>([])
const loading = ref(true)
const searchQuery = ref((route.query.q as string) || '')

/** 执行搜索 */
async function search() {
  if (!searchQuery.value.trim()) {
    articles.value = []
    return
  }
  loading.value = true
  try {
    const { data } = await getArticles({ search: searchQuery.value.trim(), page: 1, page_size: 50 })
    articles.value = data.items
  } finally {
    loading.value = false
  }
}

/** 将搜索关键词同步到 URL query，触发搜索 */
function handleSearch() {
  router.push({ name: 'search', query: { q: searchQuery.value.trim() } })
}

onMounted(search)
// URL query 变化时重新搜索（如浏览器前进后退）
watch(() => route.query.q, (q) => {
  searchQuery.value = (q as string) || ''
  search()
})
</script>

<template>
  <div>
    <h1 class="page-title">Search</h1>
    <form class="search-box" @submit.prevent="handleSearch">
      <input v-model="searchQuery" type="text" placeholder="Enter keywords..." />
      <button type="submit" class="btn btn-primary">Search</button>
    </form>
    <div v-if="loading" class="loading"><span>Loading...</span></div>
    <div v-else-if="searchQuery && articles.length === 0" class="empty">No results found for "{{ searchQuery }}".</div>
    <template v-else-if="articles.length > 0">
      <p class="result-count">Found {{ articles.length }} articles.</p>
      <ArticleCard v-for="article in articles" :key="article.id" :article="article" />
    </template>
  </div>
</template>

<style scoped lang="scss">
@use '@/assets/styles/variables' as *;

.search-box {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;

  input {
    flex: 1;
    padding: 10px 16px;
    border: 1px solid $border;
    border-radius: 4px;
    font-size: 16px;
    outline: none;

    &:focus {
      border-color: $primary;
    }
  }
}

.result-count {
  color: $text-secondary;
  margin-bottom: 16px;
}
</style>
