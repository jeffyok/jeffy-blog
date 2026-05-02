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
    <!-- 装饰渐变圆 -->
    <div class="deco-circle deco-1"></div>
    <div class="deco-circle deco-2"></div>

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
        <button type="submit" class="btn btn-primary auth-btn" :disabled="loading">
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
  position: relative;
  overflow: hidden;
  min-height: 60vh;
}

.deco-circle {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
  pointer-events: none;

  &.deco-1 {
    width: 300px;
    height: 300px;
    background: rgba(64, 158, 255, 0.3);
    top: -50px;
    left: -50px;
  }

  &.deco-2 {
    width: 250px;
    height: 250px;
    background: rgba(103, 194, 58, 0.2);
    bottom: -30px;
    right: -30px;
  }
}

.auth-form {
  width: 100%;
  max-width: 420px;
  padding: 36px;
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(30px);
  -webkit-backdrop-filter: blur(30px);
  border: 1px solid rgba(255, 255, 255, 0.4);
  position: relative;
  z-index: 1;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: $gradient-primary;
    border-radius: $radius-lg $radius-lg 0 0;
  }
}

.auth-title {
  font-size: 24px;
  text-align: center;
  margin-bottom: 28px;
  font-weight: 700;
  background: $gradient-primary;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.auth-error {
  background: rgba(245, 108, 108, 0.08);
  color: $danger;
  padding: 10px 14px;
  border-radius: $radius-sm;
  margin-bottom: 16px;
  font-size: 14px;
  border-left: 3px solid $danger;
}

.auth-btn {
  width: 100%;
  padding: 12px;
  font-size: 15px;
  font-weight: 600;
  border-radius: $radius-md;
}

.auth-link {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
  color: $text-secondary;

  a {
    color: $primary;
    font-weight: 500;

    &:hover {
      text-decoration: underline;
    }
  }
}
</style>
