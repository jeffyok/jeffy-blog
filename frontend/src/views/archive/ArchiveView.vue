<!-- 归档页面：按年月分组展示文章列表 -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getArchives } from '@/api/admin'
import type { ArchiveYear } from '@/types/api'

const archives = ref<ArchiveYear[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await getArchives()
    archives.value = data.archives
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div>
    <h1 class="page-title">文章归档</h1>
    <div v-if="loading" class="loading"><span>加载中...</span></div>
    <div v-else-if="archives.length === 0" class="empty">暂无文章。</div>
    <template v-else>
      <!-- 按年份分组 -->
      <div v-for="year in archives" :key="year.year" class="archive-year card">
        <h2 class="year-title">{{ year.year }}</h2>
        <!-- 按月份分组 -->
        <div v-for="month in year.months" :key="month.month" class="archive-month">
          <h3 class="month-title">{{ year.year }}-{{ String(month.month).padStart(2, '0') }}</h3>
          <ul class="article-list">
            <li v-for="article in month.articles" :key="article.id">
              <router-link :to="`/article/${article.slug}`">{{ article.title }}</router-link>
              <span v-if="article.author" class="author">{{ article.author.username }}</span>
              <span class="date">{{ new Date(article.created_at).toLocaleDateString() }}</span>
            </li>
          </ul>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped lang="scss">
@use '@/assets/styles/variables' as *;

.archive-year {
  margin-bottom: 24px;
}

.year-title {
  font-size: 24px;
  margin-bottom: 16px;
  color: $primary;
}

.archive-month {
  margin-bottom: 16px;
}

.month-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 8px;
}

.article-list {
  list-style: none;

  li {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
    border-bottom: 1px solid $border-light;

    a {
      color: $text;
      flex: 1;
      &:hover { color: $primary; }
    }

    .author {
      color: $text-secondary;
      font-size: 13px;
      margin: 0 12px;
    }

    .date {
      color: $text-secondary;
      font-size: 13px;
      white-space: nowrap;
    }
  }
}
</style>
