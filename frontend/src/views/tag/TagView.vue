<!-- 标签页面：根据标签 slug 展示该标签下的文章列表 -->
<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getArticles } from '@/api/articles'
import { getTags } from '@/api/tags'
import type { ArticleListItem, Tag } from '@/types/article'
import ArticleCard from '@/components/article/ArticleCard.vue'
import Pagination from '@/components/common/Pagination.vue'

const route = useRoute()
const articles = ref<ArticleListItem[]>([])
const total = ref(0)
const loading = ref(true)
const page = ref(1)
const tag = ref<Tag | null>(null)
const pageSize = 10

/** 加载标签信息并拉取该标签下的文章 */
async function loadTag() {
  loading.value = true
  try {
    // 从全部标签中找到当前 slug 对应的标签
    const tagRes = await getTags()
    tag.value = tagRes.data.find((t) => t.slug === route.params.slug) || null
    await loadArticles()
  } finally {
    loading.value = false
  }
}

/** 根据标签 ID 加载文章列表 */
async function loadArticles() {
  const { data } = await getArticles({ page: page.value, page_size: pageSize, tag_id: tag.value?.id })
  articles.value = data.items
  total.value = data.total
}

onMounted(loadTag)
watch(() => route.params.slug, loadTag)   // slug 变化时重新加载
watch(page, loadArticles)                 // 页码变化时重新加载
</script>

<template>
  <div>
    <h1 class="page-title">Tag: {{ tag?.name || route.params.slug }}</h1>
    <div v-if="loading" class="loading"><span>Loading...</span></div>
    <div v-else-if="articles.length === 0" class="empty">No articles with this tag.</div>
    <template v-else>
      <ArticleCard v-for="article in articles" :key="article.id" :article="article" />
      <Pagination :total="total" :page="page" :page-size="pageSize" @update:page="page = $event" />
    </template>
  </div>
</template>
