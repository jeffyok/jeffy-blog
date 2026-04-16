<!-- 文章卡片组件：展示文章封面、标题、摘要、标签、统计数据，点击跳转到文章详情 -->
<script setup lang="ts">
import type { ArticleListItem } from '@/types/article'

defineProps<{
  article: ArticleListItem
}>()
</script>

<template>
  <article class="article-card" @click="$router.push(`/article/${article.slug}`)">
    <!-- 封面图 -->
    <div v-if="article.cover_image" class="card-cover">
      <img :src="article.cover_image" :alt="article.title" />
    </div>
    <div class="card-body">
      <div class="card-meta">
        <span v-if="article.is_top" class="top-tag">Top</span>
        <span v-if="article.author" class="author-tag">{{ article.author.username }}</span>
        <span v-if="article.category" class="category-tag">{{ article.category.name }}</span>
        <span class="date">{{ new Date(article.created_at).toLocaleDateString() }}</span>
      </div>
      <h2 class="card-title">{{ article.title }}</h2>
      <p v-if="article.summary" class="card-summary">{{ article.summary }}</p>
      <div class="card-footer">
        <!-- 标签列表 -->
        <div class="tags">
          <span v-for="tag in article.tags" :key="tag.id" class="tag">{{ tag.name }}</span>
        </div>
        <!-- 浏览量和点赞数 -->
        <div class="stats">
          <span>👁 {{ article.view_count }}</span>
          <span>👍 {{ article.like_count }}</span>
        </div>
      </div>
    </div>
  </article>
</template>

<style scoped lang="scss">
@use '@/assets/styles/variables' as *;

.article-card {
  display: flex;
  gap: 20px;
  background: $bg-white;
  border-radius: 8px;
  padding: 20px;
  cursor: pointer;
  transition: box-shadow 0.2s, transform 0.2s;

  &:hover {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    transform: translateY(-2px);  // 悬浮上移效果
  }
}

.card-cover {
  flex-shrink: 0;               // 封面图不被压缩
  width: 200px;
  height: 140px;
  border-radius: 6px;
  overflow: hidden;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;           // 等比裁剪填充
  }
}

.card-body {
  flex: 1;
  min-width: 0;                  // 允许文本溢出省略
}

.card-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  font-size: 12px;
  color: $text-secondary;
}

.top-tag {
  background: #fef0f0;
  color: $danger;
  padding: 1px 6px;
  border-radius: 3px;
  font-weight: 600;
}

.category-tag {
  color: $primary;
}

.author-tag {
  color: $text-secondary;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 8px;
  color: $text;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;          // 标题单行省略
}

.card-summary {
  font-size: 14px;
  color: $text-secondary;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;        // 摘要最多显示两行
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stats {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: $text-secondary;
}

// 移动端改为纵向布局
@media (max-width: 768px) {
  .article-card {
    flex-direction: column;
  }

  .card-cover {
    width: 100%;
    height: 180px;
  }
}
</style>
