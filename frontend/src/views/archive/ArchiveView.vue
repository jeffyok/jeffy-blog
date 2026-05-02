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
  <div class="archive-page">
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

.archive-page {
  position: relative;
}

.archive-year {
  margin-bottom: 24px;
  position: relative;
  overflow: hidden;

  // 顶部渐变装饰条
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: $gradient-primary;
  }
}

.year-title {
  font-size: 24px;
  margin-bottom: 16px;
  background: $gradient-primary;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 700;
}

.archive-month {
  margin-bottom: 16px;
  position: relative;

  // 左侧时间线
  &::before {
    content: '';
    position: absolute;
    left: 8px;
    top: 28px;
    bottom: 0;
    width: 2px;
    background: $gradient-card-border;
  }
}

.month-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 8px;
  padding-left: 24px;
  position: relative;

  // 时间线圆点
  &::before {
    content: '';
    position: absolute;
    left: 4px;
    top: 50%;
    transform: translateY(-50%);
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: $primary;
    border: 2px solid #fff;
    box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.3);
  }
}

.article-list {
  list-style: none;

  li {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0 8px 24px;
    border-bottom: 1px solid $border-light;
    transition: all $transition-fast;
    position: relative;

    &:last-child {
      border-bottom: none;
    }

    &:hover {
      padding-left: 28px;

      &::before {
        opacity: 1;
      }
    }

    // 左侧渐变条
    &::before {
      content: '';
      position: absolute;
      left: 12px;
      top: 50%;
      transform: translateY(-50%);
      width: 3px;
      height: 0;
      border-radius: 2px;
      background: $gradient-primary;
      opacity: 0;
      transition: all $transition-fast;
    }

    &:hover::before {
      height: 60%;
      opacity: 1;
    }

    a {
      color: $text;
      flex: 1;
      transition: color $transition-fast;

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
