<!-- 管理后台仪表盘：展示博客核心统计数据 -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getDashboardStats } from '@/api/admin'
import type { DashboardStats } from '@/types/api'

const stats = ref<DashboardStats | null>(null)
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await getDashboardStats()
    stats.value = data
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div>
    <h1 class="page-title">Dashboard</h1>
    <div v-if="loading" class="loading"><span>Loading...</span></div>
    <template v-else-if="stats">
      <!-- 统计卡片网格 -->
      <div class="stats-grid">
        <div class="card stat-card">
          <div class="stat-value">{{ stats.total_articles }}</div>
          <div class="stat-label">Total Articles</div>
        </div>
        <div class="card stat-card">
          <div class="stat-value">{{ stats.published_articles }}</div>
          <div class="stat-label">Published</div>
        </div>
        <div class="card stat-card">
          <div class="stat-value">{{ stats.draft_articles }}</div>
          <div class="stat-label">Drafts</div>
        </div>
        <div class="card stat-card">
          <div class="stat-value">{{ stats.total_comments }}</div>
          <div class="stat-label">Comments</div>
        </div>
        <div class="card stat-card">
          <div class="stat-value">{{ stats.total_views }}</div>
          <div class="stat-label">Total Views</div>
        </div>
        <div class="card stat-card">
          <div class="stat-value">{{ stats.total_likes }}</div>
          <div class="stat-label">Total Likes</div>
        </div>
        <div class="card stat-card">
          <div class="stat-value">{{ stats.total_users }}</div>
          <div class="stat-label">Users</div>
        </div>
        <div class="card stat-card">
          <div class="stat-value">{{ stats.pending_comments }}</div>
          <div class="stat-label">Pending Comments</div>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped lang="scss">
@use '@/assets/styles/variables' as *;

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); // 自适应列数
  gap: 16px;
}

.stat-card {
  text-align: center;
  padding: 24px;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: $primary;
}

.stat-label {
  font-size: 14px;
  color: $text-secondary;
  margin-top: 4px;
}
</style>
