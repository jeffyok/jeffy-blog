<!-- 用户管理页面：查看/编辑/删除/重置密码 -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { adminGetUsers, adminUpdateUser, adminDeleteUser, adminResetPassword } from '@/api/admin'
import type { User } from '@/types/user'
import { formatDateTime } from '@/utils/format'
import { useAuthStore } from '@/stores/auth'
import ConfirmDialog from '@/components/common/ConfirmDialog.vue'
import Pagination from '@/components/common/Pagination.vue'

const authStore = useAuthStore()

const users = ref<User[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = 20
const loading = ref(true)

const search = ref('')
const roleFilter = ref('')
const statusFilter = ref('')

const editTarget = ref<User | null>(null)
const editForm = ref<{ role: 'admin' | 'user'; is_active: boolean }>({ role: 'user', is_active: true })

const resetTarget = ref<User | null>(null)
const resetForm = ref({ new_password: '' })

const deleteTarget = ref<User | null>(null)

async function loadUsers() {
  loading.value = true
  try {
    const params: Record<string, unknown> = { page: page.value, page_size: pageSize }
    if (search.value) params.search = search.value
    if (roleFilter.value) params.role = roleFilter.value
    if (statusFilter.value !== '') params.is_active = statusFilter.value === 'true'
    const { data } = await adminGetUsers(params as Parameters<typeof adminGetUsers>[0])
    users.value = data.items
    total.value = data.total
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  page.value = 1
  loadUsers()
}

function openEdit(user: User) {
  editTarget.value = user
  editForm.value = { role: user.role, is_active: user.is_active }
  resetTarget.value = null
}

async function handleEdit() {
  if (!editTarget.value) return
  await adminUpdateUser(editTarget.value.id, editForm.value)
  editTarget.value = null
  await loadUsers()
}

function openResetPassword(user: User) {
  resetTarget.value = user
  resetForm.value = { new_password: '' }
  editTarget.value = null
}

async function handleResetPassword() {
  if (!resetTarget.value) return
  await adminResetPassword(resetTarget.value.id, resetForm.value)
  resetTarget.value = null
}

async function handleDelete() {
  if (!deleteTarget.value) return
  await adminDeleteUser(deleteTarget.value.id)
  deleteTarget.value = null
  await loadUsers()
}

function getRoleText(role: string) {
  return role === 'admin' ? '管理员' : '普通用户'
}

function getStatusText(isActive: boolean) {
  return isActive ? '已激活' : '已禁用'
}

function isSelf(user: User) {
  return user.id === authStore.user?.id
}

onMounted(loadUsers)
</script>

<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">用户管理</h1>
    </div>

    <!-- 过滤区 -->
    <div class="filters">
      <input
        v-model="search"
        placeholder="搜索用户名或邮箱..."
        class="search-input"
        @keyup.enter="handleSearch"
      />
      <select v-model="roleFilter" @change="handleSearch">
        <option value="">全部角色</option>
        <option value="admin">管理员</option>
        <option value="user">普通用户</option>
      </select>
      <select v-model="statusFilter" @change="handleSearch">
        <option value="">全部状态</option>
        <option value="true">已激活</option>
        <option value="false">已禁用</option>
      </select>
      <button class="btn btn-sm" @click="handleSearch">搜索</button>
    </div>

    <!-- 编辑表单 -->
    <div v-if="editTarget" class="card form-card">
      <h3>编辑用户 - {{ editTarget.username }}</h3>
      <div class="form-group">
        <label>角色</label>
        <select v-model="editForm.role">
          <option value="user">普通用户</option>
          <option value="admin">管理员</option>
        </select>
      </div>
      <div class="form-group">
        <label>状态</label>
        <select v-model="editForm.is_active">
          <option :value="true">已激活</option>
          <option :value="false">已禁用</option>
        </select>
      </div>
      <div class="form-actions">
        <button class="btn" @click="editTarget = null">取消</button>
        <button class="btn btn-primary" @click="handleEdit">保存</button>
      </div>
    </div>

    <!-- 重置密码表单 -->
    <div v-if="resetTarget" class="card form-card">
      <h3>重置密码 - {{ resetTarget.username }}</h3>
      <div class="form-group">
        <label>新密码</label>
        <input v-model="resetForm.new_password" type="password" placeholder="请输入新密码（至少6位）" />
      </div>
      <div class="form-actions">
        <button class="btn" @click="resetTarget = null">取消</button>
        <button class="btn btn-primary" @click="handleResetPassword">确认重置</button>
      </div>
    </div>

    <div v-if="loading" class="loading"><span>加载中...</span></div>
    <div v-else-if="users.length === 0" class="empty">未找到用户。</div>
    <template v-else>
      <div class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>用户名</th>
              <th>邮箱</th>
              <th>角色</th>
              <th>状态</th>
              <th>注册时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.username }}</td>
              <td>{{ user.email }}</td>
              <td><span :class="['status-tag', user.role]">{{ getRoleText(user.role) }}</span></td>
              <td><span :class="['status-tag', user.is_active ? 'active' : 'disabled']">{{ getStatusText(user.is_active) }}</span></td>
              <td>{{ formatDateTime(user.created_at) }}</td>
              <td class="actions">
                <button class="btn btn-sm" @click="openEdit(user)">编辑</button>
                <button class="btn btn-sm" @click="openResetPassword(user)">重置密码</button>
                <button
                  v-if="!isSelf(user)"
                  class="btn btn-sm btn-danger"
                  @click="deleteTarget = user"
                >删除</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>

    <ConfirmDialog
      :visible="deleteTarget !== null"
      title="删除用户"
      :message="`确定要删除用户「${deleteTarget?.username}」吗？此操作不可撤销。`"
      @confirm="handleDelete"
      @cancel="deleteTarget = null"
    />

    <Pagination
      v-if="!loading && users.length > 0"
      :total="total"
      :page="page"
      :page-size="pageSize"
      @update:page="(p) => { page = p; loadUsers() }"
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
  flex-wrap: wrap;

  .search-input, select {
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

  .search-input { min-width: 200px; }
}

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

.form-group {
  margin-bottom: 12px;

  label {
    display: block;
    margin-bottom: 4px;
    font-size: 14px;
    font-weight: 500;
    color: $text;
  }

  input, select {
    width: 100%;
    max-width: 400px;
    padding: 10px 14px;
    border: 1px solid $border;
    border-radius: $radius-sm;
    font-size: 14px;
    outline: none;
    transition: all $transition-normal;

    &:focus {
      border-color: $primary;
      box-shadow: 0 0 0 3px rgba(64, 158, 255, 0.15);
    }
  }
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

  .actions { display: flex; gap: 4px; white-space: nowrap; }
}

.status-tag {
  padding: 3px 10px;
  border-radius: $radius-xl;
  font-size: 12px;
  display: inline-block;

  &.admin { background: rgba(64, 158, 255, 0.1); color: $primary; }
  &.user { background: rgba(144, 147, 153, 0.1); color: $text-secondary; }
  &.active { background: rgba(103, 194, 58, 0.1); color: $success; }
  &.disabled { background: rgba(245, 108, 108, 0.1); color: $danger; }
}
</style>
