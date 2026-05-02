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

// 每个卡片不同的渐变色
const cardGradients = [
  'linear-gradient(135deg, #409eff, #667eea)',
  'linear-gradient(135deg, #67c23a, #52b71e)',
  'linear-gradient(135deg, #e6a23c, #f5a623)',
  'linear-gradient(135deg, #667eea, #764ba2)',
  'linear-gradient(135deg, #f56c6c, #e6475b)',
  'linear-gradient(135deg, #409eff, #36d1dc)',
  'linear-gradient(135deg, #52b71e, #36d1dc)',
  'linear-gradient(135deg, #e6a23c, #f56c6c)',
]
</script>

<template>
  <div>
    <h1 class="page-title">仪表盘</h1>
    <div v-if="loading" class="loading"><span>加载中...</span></div>
    <template v-else-if="stats">
      <!-- 统计卡片网格 -->
      <div class="stats-grid">
        <div
          v-for="(item, index) in [
            { value: stats.total_articles, label: '文章总数' },
            { value: stats.published_articles, label: '已发布' },
            { value: stats.draft_articles, label: '草稿' },
            { value: stats.total_comments, label: '评论数' },
            { value: stats.total_views, label: '总浏览' },
            { value: stats.total_likes, label: '总点赞' },
            { value: stats.total_users, label: '用户数' },
            { value: stats.pending_comments, label: '待审核评论' },
          ]"
          :key="item.label"
          class="card stat-card"
        >
          <div class="stat-decoration" :style="{ background: cardGradients[index] }"></div>
          <div class="stat-value">{{ item.value }}</div>
          <div class="stat-label">{{ item.label }}</div>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped lang="scss">
@use '@/assets/styles/variables' as *;

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.stat-card {
  text-align: center;
  padding: 24px 20px;
  position: relative;
  overflow: hidden;
  transition: all $transition-normal;

  &:hover {
    transform: translateY(-4px);
    box-shadow: $shadow-lg;
  }
}

.stat-decoration {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  background: $gradient-primary;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-label {
  font-size: 14px;
  color: $text-secondary;
  margin-top: 4px;
}
</style>
