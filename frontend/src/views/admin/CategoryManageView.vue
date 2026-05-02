<!-- 分类管理页面：CRUD 分类，支持新建/编辑/删除 -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { adminGetCategories, createCategory, updateCategory, deleteCategory } from '@/api/categories'
import type { Category } from '@/types/article'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'

const categories = ref<Category[]>([])
const loading = ref(true)
const showForm = ref(false)
const editingId = ref<number | null>(null)
const form = ref({ name: '', slug: '', description: '' })
const deleteTarget = ref<number | null>(null)

async function loadCategories() {
  loading.value = true
  try {
    const { data } = await adminGetCategories()
    categories.value = data
  } finally {
    loading.value = false
  }
}

function openCreate() {
  editingId.value = null
  form.value = { name: '', slug: '', description: '' }
  showForm.value = true
}

function openEdit(cat: Category) {
  editingId.value = cat.id
  form.value = { name: cat.name, slug: cat.slug, description: cat.description || '' }
  showForm.value = true
}

async function handleSubmit() {
  if (editingId.value) {
    await updateCategory(editingId.value, form.value)
  } else {
    await createCategory(form.value)
  }
  showForm.value = false
  await loadCategories()
}

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
    <template v-else>
      <div class="table-wrapper">
        <table class="data-table">
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
      </div>
    </template>

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
  padding: 24px;
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
