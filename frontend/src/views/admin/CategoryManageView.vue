<!-- 分类管理页面：CRUD 分类，支持新建/编辑/删除 -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { adminGetCategories, createCategory, updateCategory, deleteCategory } from '@/api/categories'
import type { Category } from '@/types/article'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'

const categories = ref<Category[]>([])
const loading = ref(true)
const showForm = ref(false)
const editingId = ref<number | null>(null)  // 正在编辑的分类 ID，null 表示新建
const form = ref({ name: '', slug: '', description: '' })
const deleteTarget = ref<number | null>(null)

/** 加载分类列表 */
async function loadCategories() {
  loading.value = true
  try {
    const { data } = await adminGetCategories()
    categories.value = data
  } finally {
    loading.value = false
  }
}

/** 打开新建表单 */
function openCreate() {
  editingId.value = null
  form.value = { name: '', slug: '', description: '' }
  showForm.value = true
}

/** 打开编辑表单，填充已有数据 */
function openEdit(cat: Category) {
  editingId.value = cat.id
  form.value = { name: cat.name, slug: cat.slug, description: cat.description || '' }
  showForm.value = true
}

/** 提交表单（新建或更新） */
async function handleSubmit() {
  if (editingId.value) {
    await updateCategory(editingId.value, form.value)
  } else {
    await createCategory(form.value)
  }
  showForm.value = false
  await loadCategories()
}

/** 确认删除分类 */
async function handleDelete() {
  if (!deleteTarget.value) return
  await deleteCategory(deleteTarget.value)
  deleteTarget.value = null
  await loadCategories()
}

onMounted(loadCategories)
</script>

<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">分类管理</h1>
      <button class="btn btn-primary" @click="openCreate">新建分类</button>
    </div>

    <!-- 新建/编辑表单 -->
    <div v-if="showForm" class="card form-card">
      <h3>{{ editingId ? '编辑' : '新建' }}分类</h3>
      <div class="form-group">
        <label>名称</label>
        <input v-model="form.name" />
      </div>
      <div class="form-group">
        <label>别名</label>
        <input v-model="form.slug" placeholder="留空则自动生成" />
      </div>
      <div class="form-group">
        <label>描述</label>
        <input v-model="form.description" />
      </div>
      <div class="form-actions">
        <button class="btn" @click="showForm = false">取消</button>
        <button class="btn btn-primary" @click="handleSubmit">保存</button>
      </div>
    </div>

    <div v-if="loading" class="loading"><span>加载中...</span></div>
    <!-- 分类数据表格 -->
    <table v-else class="data-table">
      <thead>
        <tr>
          <th>名称</th>
          <th>别名</th>
          <th>描述</th>
          <th>创建时间</th>
          <th>操作</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="cat in categories" :key="cat.id">
          <td>{{ cat.name }}</td>
          <td>{{ cat.slug }}</td>
          <td>{{ cat.description || '-' }}</td>
          <td>{{ new Date(cat.created_at).toLocaleString('zh-CN') }}</td>
          <td class="actions">
            <button class="btn btn-sm" @click="openEdit(cat)">编辑</button>
            <button class="btn btn-sm btn-danger" @click="deleteTarget = cat.id">删除</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- 删除确认对话框 -->
    <ConfirmDialog
      :visible="deleteTarget !== null"
      title="删除分类"
      message="确定要删除这个分类吗？"
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
