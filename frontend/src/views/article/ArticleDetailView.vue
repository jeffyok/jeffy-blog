<!-- 文章详情页：文章内容 + 目录侧边栏 + 评论区 -->
<script setup lang="ts">
import { ref, onMounted, nextTick, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getArticle } from '@/api/articles'
import type { Article } from '@/types/article'
import { formatDate } from '@/utils/format'
import LikeButton from '@/components/article/LikeButton.vue'
import CommentSection from '@/components/article/CommentSection.vue'

const route = useRoute()
const article = ref<Article | null>(null)
const loading = ref(true)
const tocHeadings = ref<{ id: string; text: string; level: number }[]>([])
const activeTocId = ref('')

onMounted(async () => {
  await loadArticle()
})

// slug 变化时重新加载（如从一篇文章跳到另一篇）
watch(() => route.params.slug, async () => {
  await loadArticle()
})

/** 加载文章详情并提取目录 */
async function loadArticle() {
  loading.value = true
  try {
    const { data } = await getArticle(route.params.slug as string)
    article.value = data
    await nextTick()
    extractToc()
  } catch {
    article.value = null
  } finally {
    loading.value = false
  }
}

/** 从 markdown 渲染内容中提取 h2/h3 作为目录 */
function extractToc() {
  const contentEl = document.querySelector('.markdown-content')
  if (!contentEl) return
  const headings = contentEl.querySelectorAll('h2, h3')
  tocHeadings.value = Array.from(headings).map((el) => ({
    id: el.id || '',
    text: el.textContent || '',
    level: parseInt(el.tagName[1]),
  }))
  if (tocHeadings.value.length > 0 && !activeTocId.value) {
    activeTocId.value = tocHeadings.value[0].id
  }
  setupScrollSpy()
}

/** 滚动到指定标题 */
function scrollToHeading(id: string) {
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' })
}

/** 使用 IntersectionObserver 监听滚动，高亮当前可见的目录项 */
function setupScrollSpy() {
  const contentEl = document.querySelector('.markdown-content')
  if (!contentEl) return

  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          activeTocId.value = entry.target.id
        }
      }
    },
    { rootMargin: '-80px 0px -80% 0px', root: null }
  )

  tocHeadings.value.forEach(({ id }) => {
    const el = document.getElementById(id)
    if (el) observer.observe(el)
  })
}
</script>

<template>
  <div class="article-detail-page">
    <div v-if="loading" class="loading"><span>加载中...</span></div>
    <template v-else-if="article">
      <div class="main-column">
        <!-- 文章主体 -->
        <article class="card article-content">
          <div class="article-header">
            <span v-if="article.is_top" class="top-tag">置顶</span>
            <h1 class="article-title">{{ article.title }}</h1>
          </div>
          <div class="article-meta">
            <span v-if="article.author">{{ article.author.username }}</span>
            <span>{{ formatDate(article.created_at) }}</span>
            <span v-if="article.category">
              <router-link :to="`/category/${article.category.slug}`">{{ article.category.name }}</router-link>
            </span>
            <span>👁 {{ article.view_count }}</span>
          </div>
          <div v-if="article.tags.length" class="article-tags">
            <router-link v-for="tag in article.tags" :key="tag.id" :to="`/tag/${tag.slug}`" class="tag">{{ tag.name }}</router-link>
          </div>
          <!-- markdown 渲染内容 -->
          <div class="markdown-content" v-html="article.content_html || article.content" />
          <div class="article-actions">
            <LikeButton :article-id="article.id" :like-count="article.like_count" />
          </div>
        </article>
        <!-- 评论区 -->
        <CommentSection :article-id="article.id" />
      </div>

      <!-- 目录侧边栏（仅在存在标题时显示） -->
      <aside v-if="tocHeadings.length" class="toc-sidebar">
        <div class="card">
          <h3 class="toc-title">目录</h3>
          <nav class="toc-list">
            <a
              v-for="heading in tocHeadings"
              :key="heading.id"
              :href="`#${heading.id}`"
              :class="['toc-item', `level-${heading.level}`, { active: activeTocId === heading.id }]"
              @click.prevent="scrollToHeading(heading.id)"
            >
              {{ heading.text }}
            </a>
          </nav>
        </div>
      </aside>
    </template>
    <div v-else class="empty">文章未找到。</div>
  </div>
</template>

<style scoped lang="scss">
@use '@/assets/styles/variables' as *;
@use '@/assets/styles/markdown';

.article-detail-page {
  display: flex;
  gap: 24px;
}

.main-column {
  flex: 1;
  min-width: 0;
}

.article-content {
  padding: 32px;
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

.article-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.article-title {
  font-size: 28px;
  margin: 0;
  position: relative;
  padding-bottom: 16px;

  // 标题下方渐变分割线
  &::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 60px;
    height: 3px;
    border-radius: 2px;
    background: $gradient-primary;
  }
}

.top-tag {
  padding: 3px 10px;
  background: $gradient-primary;
  color: #fff;
  font-size: 12px;
  border-radius: $radius-xl;
  white-space: nowrap;
}

.article-meta {
  display: flex;
  gap: 16px;
  color: $text-secondary;
  font-size: 14px;
  margin-bottom: 16px;
}

.article-tags {
  margin-bottom: 24px;
}

.article-actions {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid $border-light;
  position: relative;

  &::before {
    content: '';
    position: absolute;
    top: -1px;
    left: 0;
    width: 60px;
    height: 2px;
    background: $gradient-card-border;
  }
}

// 目录侧边栏：固定定位，跟随滚动
.toc-sidebar {
  width: 240px;
  flex-shrink: 0;
  position: sticky;
  top: 84px;
  height: fit-content;
  max-height: calc(100vh - 100px);
  overflow-y: auto;
}

.toc-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
  padding-left: 12px;
  position: relative;

  &::before {
    content: '';
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 3px;
    height: 16px;
    border-radius: 2px;
    background: $gradient-primary;
  }
}

.toc-list {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.toc-item {
  display: block;
  padding: 6px 12px;
  font-size: 14px;
  color: $text-secondary;
  text-decoration: none;
  border-left: 2px solid transparent;
  border-radius: 0 $radius-sm $radius-sm 0;
  transition: all $transition-fast;

  &:hover {
    color: $primary;
    background: rgba(64, 158, 255, 0.04);
  }

  &.level-3 {
    padding-left: 24px;
  }

  &.active {
    color: $primary;
    border-left-color: $primary;
    background: rgba(64, 158, 255, 0.08);
    font-weight: 500;
  }
}

// 中等屏幕以下隐藏目录
@media (max-width: 1024px) {
  .toc-sidebar {
    display: none;
  }
}
</style>
