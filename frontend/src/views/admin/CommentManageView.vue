<!-- 评论管理页面：审核/拒绝/删除评论 -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { adminGetComments, updateCommentStatus, deleteComment } from '@/api/comments'
import type { Comment } from '@/types/comment'
import { formatDateTime } from '@/utils/format'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import Pagination from '@/components/common/Pagination.vue'

const comments = ref<Comment[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = 20
const loading = ref(true)
const statusFilter = ref('')
const deleteTarget = ref<number | null>(null)

function getStatusText(status: string) {
  const statusMap: Record<string, string> = { pending: '待审核', approved: '已通过', rejected: '已拒绝' }
  return statusMap[status] || status
}

async function loadComments() {
  loading.value = true
  try {
    const params: Record<string, unknown> = { page: page.value, page_size: pageSize }
    if (statusFilter.value) params.status = statusFilter.value
    const { data } = await adminGetComments(params as Parameters<typeof adminGetComments>[0])
    comments.value = data.items
    total.value = data.total
  } finally {
    loading.value = false
  }
}

async function approve(commentId: number) {
  await updateCommentStatus(commentId, 'approved')
  await loadComments()
}

async function reject(commentId: number) {
  await updateCommentStatus(commentId, 'rejected')
  await loadComments()
}

async function handleDelete() {
  if (!deleteTarget.value) return
  await deleteComment(deleteTarget.value)
  deleteTarget.value = null
  await loadComments()
}

onMounted(loadComments)
</script>

<template>
  <div>
    <h1 class="page-title">评论管理</h1>

    <div class="filters">
      <select v-model="statusFilter" @change="page = 1; loadComments()">
        <option value="">全部状态</option>
        <option value="pending">待审核</option>
        <option value="approved">已通过</option>
        <option value="rejected">已拒绝</option>
      </select>
    </div>

    <div v-if="loading" class="loading"><span>加载中...</span></div>
    <div v-else-if="comments.length === 0" class="empty">未找到评论。</div>
    <template v-else>
      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>内容</th>
              <th>作者</th>
              <th>状态</th>
              <th>时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="comment in comments" :key="comment.id">
              <td class="content-cell">{{ comment.content }}</td>
              <td>{{ comment.user?.username || comment.nickname || '游客' }}</td>
              <td><span :class="['status-tag', comment.status]">{{ getStatusText(comment.status) }}</span></td>
              <td>{{ formatDateTime(comment.created_at) }}</td>
              <td class="actions">
                <button v-if="comment.status !== 'approved'" class="btn btn-sm" @click="approve(comment.id)">通过</button>
                <button v-if="comment.status !== 'rejected'" class="btn btn-sm" @click="reject(comment.id)">拒绝</button>
                <button class="btn btn-sm btn-danger" @click="deleteTarget = comment.id">删除</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>

    <ConfirmDialog
      :visible="deleteTarget !== null"
      title="删除评论"
      message="确定要删除这条评论吗？"
      @confirm="handleDelete"
      @cancel="deleteTarget = null"
    />

    <Pagination
      v-if="!loading && comments.length > 0"
      :total="total"
      :page="page"
      :page-size="pageSize"
      @update:page="(p) => { page = p; loadComments() }"
    />
  </div>
</template>

<style scoped lang="scss">
@use '@/assets/styles/variables' as *;

.filters {
  margin-bottom: 16px;

  select {
    padding: 8px 14px;
    border: 1px solid $border;
    border-radius: $radius-sm;
    font-size: 14px;
    outline: none;
    background: $bg-white;
    transition: all $transition-normal;

    &:focus {
      border-color: $primary;
      box-shadow: 0 0 0 3px rgba(64, 158, 255, 0.15);
    }
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

  .actions { display: flex; gap: 4px; white-space: nowrap; }

  .content-cell {
    max-width: 300px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}
</style>
