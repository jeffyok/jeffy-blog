<!-- 注册页面 -->
<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const error = ref('')
const loading = ref(false)

/** 处理注册 */
async function handleRegister() {
  error.value = ''
  if (password.value !== confirmPassword.value) {
    error.value = '两次输入的密码不一致'
    return
  }
  loading.value = true
  try {
    await authStore.register(username.value, email.value, password.value)
    // 注册成功后自动登录
    await authStore.login(username.value, password.value)
    router.push('/')
  } catch (e: unknown) {
    error.value = typeof e === 'object' && e !== null && 'response' in e
      ? ((e as { response: { data: { detail?: string } } }).response?.data?.detail || '注册失败')
      : '注册失败'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="auth-page">
    <div class="card auth-form">
      <h1 class="auth-title">注册</h1>
      <!-- 错误提示 -->
      <div v-if="error" class="auth-error">{{ error }}</div>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label>用户名</label>
          <input v-model="username" type="text" required />
        </div>
        <div class="form-group">
          <label>邮箱</label>
          <input v-model="email" type="email" required />
        </div>
        <div class="form-group">
          <label>密码</label>
          <input v-model="password" type="password" required minlength="6" />
        </div>
        <div class="form-group">
          <label>确认密码</label>
          <input v-model="confirmPassword" type="password" required />
        </div>
        <button type="submit" class="btn btn-primary" style="width: 100%;" :disabled="loading">
          {{ loading ? '注册中...' : '注册' }}
        </button>
      </form>
      <p class="auth-link">
        已有账号？ <router-link to="/login">登录</router-link>
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
