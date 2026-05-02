<!-- 管理后台文章列表页：搜索、过滤、编辑、删除文章 -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { adminGetArticles, deleteArticle } from '@/api/articles'
import type { ArticleListItem } from '@/types/article'
import { formatDateTime } from '@/utils/format'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import Pagination from '@/components/common/Pagination.vue'

const articles = ref<ArticleListItem[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = 20
const loading = ref(true)
const deleteTarget = ref<number | null>(null)
const search = ref('')
const statusFilter = ref('')

function getStatusText(status: string) {
  const statusMap: Record<string, string> = { draft: '草稿', published: '已发布' }
  return statusMap[status] || status
}

async function loadArticles() {
  loading.value = true
  try {
    const params: Record<string, unknown> = { page: page.value, page_size: pageSize }
    if (statusFilter.value !== '') params.status = statusFilter.value
    if (search.value) params.search = search.value
    const { data } = await adminGetArticles(params as Parameters<typeof adminGetArticles>[0])
    articles.value = data.items
    total.value = data.total
  } finally {
    loading.value = false
  }
}

async function handleDelete() {
  if (!deleteTarget.value) return
  await deleteArticle(deleteTarget.value)
  deleteTarget.value = null
  await loadArticles()
}

function handleSearch() {
  page.value = 1
  loadArticles()
}

onMounted(loadArticles)
</script>

<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">文章管理</h1>
      <router-link to="/admin/articles/new" class="btn btn-primary">新建文章</router-link>
    </div>

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
      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>标题</th>
              <th>状态</th>
              <th>分类</th>
              <th>作者</th>
              <th>浏览</th>
              <th>点赞</th>
              <th>创建时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="article in articles" :key="article.id">
              <td>{{ article.title }}</td>
              <td><span :class="['status-tag', article.status]">{{ getStatusText(article.status) }}</span></td>
              <td>{{ article.category?.name || '-' }}</td>
              <td>{{ article.author?.username || '-' }}</td>
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
      </div>
    </template>

    <ConfirmDialog
      :visible="deleteTarget !== null"
      title="删除文章"
      message="确定要删除这篇文章吗？此操作无法撤销。"
      @confirm="handleDelete"
      @cancel="deleteTarget = null"
    />

    <Pagination
      v-if="!loading && articles.length > 0"
      :total="total"
      :page="page"
      :page-size="pageSize"
      @update:page="(p) => { page = p; loadArticles() }"
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

.page-title { margin-bottom: 0; }

.filters {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;

  input, select {
    padding: 8px 14px;
    border: 1px solid $border;
    border-radius: $radius-sm;
    font-size: 14px;
    outline: none;
    transition: all $transition-normal;
    background: $bg-white;

    &:focus {
      border-color: $primary;
      box-shadow: 0 0 0 3px rgba(64, 158, 255, 0.15);
    }
  }

  input {
    flex: 1;
    max-width: 300px;
  }
}

.table-wrapper {
  border-radius: $radius-lg;
  overflow: hidden;
  box-shadow: $shadow-md;
  border: 1px solid $glass-border;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  background: $bg-white;

  th, td {
    padding: 12px 16px;
    text-align: left;
    border-bottom: 1px solid $border-light;
    font-size: 14px;
  }

  th {
    background: $gradient-primary;
    color: #fff;
    font-weight: 600;
    font-size: 13px;
  }

  tbody tr {
    transition: background $transition-fast;

    &:hover {
      background: rgba(64, 158, 255, 0.04);
    }
  }

  .actions {
    display: flex;
    gap: 4px;
  }
}

@media (max-width: 768px) {
  .data-table {
    font-size: 12px;

    th, td {
      padding: 8px;
    }
  }
}
</style>
