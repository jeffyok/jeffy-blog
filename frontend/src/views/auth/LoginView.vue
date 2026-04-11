<!-- 登录页面 -->
<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

/** 处理登录 */
async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    await authStore.login(username.value, password.value)
    router.push('/')              // 登录成功跳转首页
  } catch (e: unknown) {
    const msg = e instanceof Error ? e.message : 'Login failed'
    // 尝试从后端响应中提取错误详情
    error.value = typeof e === 'object' && e !== null && 'response' in e
      ? ((e as { response: { data: { detail?: string } } }).response?.data?.detail || msg)
      : msg
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="auth-page">
    <div class="card auth-form">
      <h1 class="auth-title">Login</h1>
      <!-- 错误提示 -->
      <div v-if="error" class="auth-error">{{ error }}</div>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Username</label>
          <input v-model="username" type="text" required />
        </div>
        <div class="form-group">
          <label>Password</label>
          <input v-model="password" type="password" required />
        </div>
        <button type="submit" class="btn btn-primary" style="width: 100%;" :disabled="loading">
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>
      <p class="auth-link">
        Don't have an account? <router-link to="/register">Register</router-link>
      </p>
    </div>
  </div>
</template>

<style scoped lang="scss">
@use '@/assets/styles/variables' as *;

.auth-page {
  display: flex;
  justify-content: center;
  padding: 40px 0;
}

.auth-form {
  width: 100%;
  max-width: 400px;
  padding: 32px;
}

.auth-title {
  font-size: 24px;
  text-align: center;
  margin-bottom: 24px;
}

.auth-error {
  background: #fef0f0;
  color: $danger;
  padding: 8px 12px;
  border-radius: 4px;
  margin-bottom: 16px;
  font-size: 14px;
}

.auth-link {
  text-align: center;
  margin-top: 16px;
  font-size: 14px;
  color: $text-secondary;
}
</style>
