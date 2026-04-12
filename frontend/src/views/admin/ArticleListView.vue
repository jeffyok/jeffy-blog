<!-- 管理后台文章列表页：搜索、过滤、编辑、删除文章 -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getArticles, deleteArticle } from '@/api/articles'
import type { ArticleListItem } from '@/types/article'
import { formatDateTime } from '@/utils/format'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'

const router = useRouter()
const articles = ref<ArticleListItem[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = 20
const loading = ref(true)
const deleteTarget = ref<number | null>(null)  // 待删除的文章 ID
const search = ref('')
const statusFilter = ref('')

/** 加载文章列表（支持搜索和状态过滤） */
async function loadArticles() {
  loading.value = true
  try {
    const params: Record<string, unknown> = { page: page.value, page_size: pageSize, status: 'all' }
    if (statusFilter.value) params.status = statusFilter.value
    if (search.value) params.search = search.value
    const { data } = await getArticles(params as Parameters<typeof getArticles>[0])
    articles.value = data.items
    total.value = data.total
  } finally {
    loading.value = false
  }
}

/** 确认删除文章 */
async function handleDelete() {
  if (!deleteTarget.value) return
  await deleteArticle(deleteTarget.value)
  deleteTarget.value = null
  await loadArticles()
}

/** 搜索（重置页码为 1） */
function handleSearch() {
  page.value = 1
  loadArticles()
}

onMounted(loadArticles)
</script>

<template>
  <div>
    <!-- 页头：标题 + 新建按钮 -->
    <div class="page-header">
      <h1 class="page-title">文章管理</h1>
      <router-link to="/admin/articles/new" class="btn btn-primary">新建文章</router-link>
    </div>

    <!-- 搜索和状态过滤 -->
    <div class="filters">
      <input v-model="search" placeholder="搜索文章..." @keyup.enter="handleSearch" />
      <select v-model="statusFilter" @change="page = 1; loadArticles()">
        <option value="">全部状态</option>
        <option value="published">已发布</option>
        <option value="draft">草稿</option>
      </select>
    </div>

    <div v-if="loading" class="loading"><span>加载中...</span></div>
    <div v-else-if="articles.length === 0" class="empty">未找到文章。</div>
    <template v-else>
      <!-- 文章数据表格 -->
      <table class="data-table">
        <thead>
          <tr>
            <th>标题</th>
            <th>状态</th>
            <th>分类</th>
            <th>浏览</th>
            <th>点赞</th>
            <th>创建时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="article in articles" :key="article.id">
            <td>{{ article.title }}</td>
            <td><span :class="['status-tag', article.status]">{{ article.status }}</span></td>
            <td>{{ article.category?.name || '-' }}</td>
            <td>{{ article.view_count }}</td>
            <td>{{ article.like_count }}</td>
            <td>{{ formatDateTime(article.created_at) }}</td>
            <td class="actions">
              <router-link :to="`/admin/articles/${article.id}/edit`" class="btn btn-sm">编辑</router-link>
              <button class="btn btn-sm btn-danger" @click="deleteTarget = article.id">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </template>

    <!-- 删除确认对话框 -->
    <ConfirmDialog
      :visible="deleteTarget !== null"
      title="删除文章"
      message="确定要删除这篇文章吗？此操作无法撤销。"
      @confirm="handleDelete"
      @cancel="deleteTarget = null"
    />
  </div>
</template>

<style scoped lang="scss">
@use '@/assets/styles/variables' as *;

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.page-title {
  margin-bottom: 0;
}

.filters {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;

  input, select {
    padding: 8px 12px;
    border: 1px solid $border;
    border-radius: 4px;
    font-size: 14px;
    outline: none;

    &:focus {
      border-color: $primary;
    }
  }

  input {
    flex: 1;
    max-width: 300px;
  }
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  background: $bg-white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);

  th, td {
    padding: 12px 16px;
    text-align: left;
    border-bottom: 1px solid $border-light;
    font-size: 14px;
  }

  th {
    background: $bg;
    font-weight: 600;
  }

  .actions {
    display: flex;
    gap: 4px;
  }
}

// 移动端表格紧凑显示
@media (max-width: 768px) {
  .data-table {
    font-size: 12px;

    th, td {
      padding: 8px;
    }
  }
}
</style>
