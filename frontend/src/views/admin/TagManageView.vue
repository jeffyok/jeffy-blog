<!-- 标签管理页面：CRUD 标签，支持新建/编辑/删除 -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getTags, createTag, updateTag, deleteTag } from '@/api/tags'
import type { Tag } from '@/types/article'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'

const tags = ref<Tag[]>([])
const loading = ref(true)
const showForm = ref(false)
const editingId = ref<number | null>(null)  // 正在编辑的标签 ID，null 表示新建
const form = ref({ name: '', slug: '' })
const deleteTarget = ref<number | null>(null)

/** 加载标签列表 */
async function loadTags() {
  loading.value = true
  try {
    const { data } = await getTags()
    tags.value = data
  } finally {
    loading.value = false
  }
}

/** 打开新建表单 */
function openCreate() {
  editingId.value = null
  form.value = { name: '', slug: '' }
  showForm.value = true
}

/** 打开编辑表单，填充已有数据 */
function openEdit(tag: Tag) {
  editingId.value = tag.id
  form.value = { name: tag.name, slug: tag.slug }
  showForm.value = true
}

/** 提交表单（新建或更新） */
async function handleSubmit() {
  if (editingId.value) {
    await updateTag(editingId.value, form.value)
  } else {
    await createTag(form.value)
  }
  showForm.value = false
  await loadTags()
}

/** 确认删除标签 */
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
      <h1 class="page-title">Tags</h1>
      <button class="btn btn-primary" @click="openCreate">New Tag</button>
    </div>

    <!-- 新建/编辑表单 -->
    <div v-if="showForm" class="card form-card">
      <h3>{{ editingId ? 'Edit' : 'New' }} Tag</h3>
      <div class="form-group">
        <label>Name</label>
        <input v-model="form.name" />
      </div>
      <div class="form-group">
        <label>Slug</label>
        <input v-model="form.slug" placeholder="auto-generated if empty" />
      </div>
      <div class="form-actions">
        <button class="btn" @click="showForm = false">Cancel</button>
        <button class="btn btn-primary" @click="handleSubmit">Save</button>
      </div>
    </div>

    <div v-if="loading" class="loading"><span>Loading...</span></div>
    <!-- 标签数据表格 -->
    <table v-else class="data-table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Slug</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="tag in tags" :key="tag.id">
          <td>{{ tag.name }}</td>
          <td>{{ tag.slug }}</td>
          <td class="actions">
            <button class="btn btn-sm" @click="openEdit(tag)">Edit</button>
            <button class="btn btn-sm btn-danger" @click="deleteTarget = tag.id">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- 删除确认对话框 -->
    <ConfirmDialog
      :visible="deleteTarget !== null"
      title="Delete Tag"
      message="Are you sure you want to delete this tag?"
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
  padding: 20px;

  h3 { margin-bottom: 16px; }
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
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

  th { background: $bg; font-weight: 600; }
  .actions { display: flex; gap: 4px; }
}
</style>
