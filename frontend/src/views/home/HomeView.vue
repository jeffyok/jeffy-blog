<!-- 首页：文章列表 + 侧边栏（分类和标签） -->
<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useArticlesStore } from '@/stores/articles'
import ArticleCard from '@/components/article/ArticleCard.vue'
import Pagination from '@/components/common/Pagination.vue'
import { getCategories } from '@/api/categories'
import { getTags } from '@/api/tags'
import type { Category } from '@/types/article'
import type { Tag } from '@/types/article'

const store = useArticlesStore()
const categories = ref<Category[]>([])
const tags = ref<Tag[]>([])
const page = ref(1)
const pageSize = 10

onMounted(async () => {
  // 并行加载文章列表和侧边栏数据
  await Promise.all([
    store.fetchArticles({ page: 1, page_size: pageSize }),
    loadSidebar(),
  ])
})

// 页码变化时重新加载文章
watch(page, (newPage) => {
  store.fetchArticles({ page: newPage, page_size: pageSize })
})

/** 加载侧边栏分类和标签 */
async function loadSidebar() {
  try {
    const [catRes, tagRes] = await Promise.all([getCategories(), getTags()])
    categories.value = catRes.data
    tags.value = tagRes.data
  } catch { /* ignore */ }
}
</script>

<template>
  <div class="home-page">
    <!-- 左侧主内容：文章列表 -->
    <div class="main-column">
      <h1 class="page-title">Latest Articles</h1>
      <div v-if="store.loading" class="loading"><span>Loading...</span></div>
      <div v-else-if="store.articles.length === 0" class="empty">No articles yet.</div>
      <template v-else>
        <ArticleCard v-for="article in store.articles" :key="article.id" :article="article" />
        <Pagination :total="store.total" :page="page" :page-size="pageSize" @update:page="page = $event" />
      </template>
    </div>
    <!-- 右侧边栏 -->
    <aside class="sidebar">
      <!-- 分类列表 -->
      <div v-if="categories.length" class="card sidebar-section">
        <h3 class="sidebar-title">Categories</h3>
        <ul class="sidebar-list">
          <li v-for="cat in categories" :key="cat.id">
            <router-link :to="`/category/${cat.slug}`">{{ cat.name }}</router-link>
          </li>
        </ul>
      </div>
      <!-- 标签云 -->
      <div v-if="tags.length" class="card sidebar-section">
        <h3 class="sidebar-title">Tags</h3>
        <div class="tag-cloud">
          <router-link v-for="tag in tags" :key="tag.id" :to="`/tag/${tag.slug}`" class="tag">{{ tag.name }}</router-link>
        </div>
      </div>
    </aside>
  </div>
</template>

<style scoped lang="scss">
@use '@/assets/styles/variables' as *;

.home-page {
  display: flex;
  gap: 24px;
}

.main-column {
  flex: 1;
  min-width: 0;
}

.main-column > .article-card + .article-card {
  margin-top: 16px;             // 文章卡片之间的间距
}

.sidebar {
  width: $sidebar-width;
  flex-shrink: 0;
}

.sidebar-section {
  margin-bottom: 16px;
}

.sidebar-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid $border-light;
}

.sidebar-list {
  list-style: none;

  li {
    padding: 4px 0;

    a {
      color: $text;
      font-size: 14px;

      &:hover {
        color: $primary;
      }
    }
  }
}

.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

// 移动端改为单列布局
@media (max-width: 768px) {
  .home-page {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
  }
}
</style>
