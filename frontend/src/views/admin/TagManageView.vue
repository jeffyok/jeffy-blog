<!-- 标签管理页面：CRUD 标签，支持新建/编辑/删除 -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { adminGetTags, createTag, updateTag, deleteTag } from '@/api/tags'
import type { Tag } from '@/types/article'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'

const tags = ref<Tag[]>([])
const loading = ref(true)
const showForm = ref(false)
const editingId = ref<number | null>(null)
const form = ref({ name: '', slug: '' })
const deleteTarget = ref<number | null>(null)

async function loadTags() {
  loading.value = true
  try {
    const { data } = await adminGetTags()
    tags.value = data
  } finally {
    loading.value = false
  }
}

function openCreate() {
  editingId.value = null
  form.value = { name: '', slug: '' }
  showForm.value = true
}

function openEdit(tag: Tag) {
  editingId.value = tag.id
  form.value = { name: tag.name, slug: tag.slug }
  showForm.value = true
}

async function handleSubmit() {
  if (editingId.value) {
    await updateTag(editingId.value, form.value)
  } else {
    await createTag(form.value)
  }
  showForm.value = false
  await loadTags()
}

async function handleDelete() {
  if (!deleteTarget.value) return
  await deleteTag(deleteTarget.value)
  deleteTarget.value = null
  await loadTags()
}

onMounted(loadTags)
</script>

<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">标签管理</h1>
      <button class="btn btn-primary" @click="openCreate">新建标签</button>
    </div>

    <!-- 新建/编辑表单 -->
    <div v-if="showForm" class="card form-card">
      <h3>{{ editingId ? '编辑' : '新建' }}标签</h3>
      <div class="form-group">
        <label>名称</label>
        <input v-model="form.name" />
      </div>
      <div class="form-group">
        <label>别名</label>
        <input v-model="form.slug" placeholder="留空则自动生成" />
      </div>
      <div class="form-actions">
        <button class="btn" @click="showForm = false">取消</button>
        <button class="btn btn-primary" @click="handleSubmit">保存</button>
      </div>
    </div>

    <div v-if="loading" class="loading"><span>加载中...</span></div>
    <template v-else>
      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>名称</th>
              <th>别名</th>
              <th>创建时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="tag in tags" :key="tag.id">
              <td>{{ tag.name }}</td>
              <td>{{ tag.slug }}</td>
              <td>{{ new Date(tag.created_at).toLocaleString('zh-CN') }}</td>
              <td class="actions">
                <button class="btn btn-sm" @click="openEdit(tag)">编辑</button>
                <button class="btn btn-sm btn-danger" @click="deleteTarget = tag.id">删除</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>

    <ConfirmDialog
      :visible="deleteTarget !== null"
      title="删除标签"
      message="确定要删除这个标签吗？"
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

.page-title { margin-bottom: 0; }

.form-card {
  margin-bottom: 16px;
  padding: 24px;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: $gradient-primary;
  }

  h3 { margin-bottom: 16px; font-weight: 600; }
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
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

  .actions { display: flex; gap: 4px; }
}
</style>
