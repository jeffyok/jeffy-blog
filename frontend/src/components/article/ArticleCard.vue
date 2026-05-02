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
      <div class="cover-overlay"></div>
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
  background: $glass-card-bg;
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-radius: $radius-lg;
  padding: 20px;
  border: 1px solid $glass-border;
  cursor: pointer;
  transition: all $transition-normal;
  position: relative;

  &:hover {
    box-shadow: $shadow-lg;
    transform: translateY(-4px);
    border-color: rgba(64, 158, 255, 0.2);

    .card-cover img {
      transform: scale(1.05);
    }

    .cover-overlay {
      opacity: 1;
    }
  }
}

.card-cover {
  flex-shrink: 0;
  width: 200px;
  height: 140px;
  border-radius: $radius-md;
  overflow: hidden;
  position: relative;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform $transition-slow;
  }
}

.cover-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(64, 158, 255, 0.1) 0%, rgba(102, 126, 234, 0.1) 100%);
  opacity: 0;
  transition: opacity $transition-normal;
}

.card-body {
  flex: 1;
  min-width: 0;
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
  background: rgba(245, 108, 108, 0.1);
  color: $danger;
  padding: 1px 8px;
  border-radius: $radius-xl;
  font-weight: 600;
}

.category-tag {
  color: $primary;
  font-weight: 500;
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
  white-space: nowrap;
  transition: color $transition-fast;

  .article-card:hover & {
    color: $primary;
  }
}

.card-summary {
  font-size: 14px;
  color: $text-secondary;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.6;
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
  transition: color $transition-fast;

  .article-card:hover & {
    color: $primary-light;
  }
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
