<!-- 前台顶部导航栏：Logo + 导航链接 + 搜索框 + 移动端菜单 -->
<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const mobileMenuOpen = ref(false)
const searchKeyword = ref('')

/** 关闭移动端菜单 */
function closeMenu() {
  mobileMenuOpen.value = false
}

/** 切换移动端菜单 */
function toggleMenu() {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

/** 提交搜索，跳转到搜索页面 */
function handleSearch() {
  if (searchKeyword.value.trim()) {
    router.push({ name: 'search', query: { q: searchKeyword.value.trim() } })
    searchKeyword.value = ''
    closeMenu()
  }
}

/** 退出登录 */
function logout() {
  authStore.logout()
  router.push('/')
}
</script>

<template>
  <header class="app-header">
    <div class="container header-inner">
      <router-link to="/" class="logo">Jeffy Blog</router-link>
      <!-- 导航链接（移动端可展开） -->
      <nav class="nav-links" :class="{ open: mobileMenuOpen }">
        <router-link to="/" @click="closeMenu">首页</router-link>
        <router-link to="/archive" @click="closeMenu">归档</router-link>
        <router-link to="/friends" @click="closeMenu">友情链接</router-link>
        <router-link to="/about" @click="closeMenu">关于</router-link>
        <!-- 仅管理员可见的后台入口 -->
        <template v-if="authStore.isAdmin">
          <router-link to="/admin" @click="closeMenu">管理后台</router-link>
        </template>
        <!-- 移动端：已登录显示用户名和退出，未登录显示登录 -->
        <div class="mobile-user-section">
          <template v-if="authStore.isLoggedIn">
            <span class="mobile-username">用户：{{ authStore.user?.username }}</span>
            <a href="#" @click.prevent="logout(); closeMenu()">退出</a>
          </template>
          <template v-else>
            <router-link to="/login" @click="closeMenu">登录</router-link>
          </template>
        </div>
      </nav>
      <!-- 右侧区域：搜索框 + 用户信息 -->
      <div class="header-right">
        <!-- 搜索表单 -->
        <form class="search-form" @submit.prevent="handleSearch">
          <input v-model="searchKeyword" type="text" placeholder="搜索..." class="search-input" />
        </form>
        <!-- 用户信息区域 -->
        <div v-if="authStore.isLoggedIn" class="user-menu">
          <div class="username">{{ authStore.user?.username }}</div>
          <a href="#" @click.prevent="logout" class="logout-link">退出</a>
        </div>
        <router-link v-else to="/login" class="login-link">登录</router-link>
      </div>
      <!-- 移动端汉堡菜单按钮 -->
      <button class="mobile-toggle" :class="{ active: mobileMenuOpen }" @click="toggleMenu">
        <span></span>
        <span></span>
        <span></span>
      </button>
    </div>
  </header>
</template>

<style scoped lang="scss">
@use '@/assets/styles/variables' as *;

.app-header {
  background: $glass-bg;
  backdrop-filter: blur(20px) saturate(1.8);
  -webkit-backdrop-filter: blur(20px) saturate(1.8);
  border-bottom: 1px solid rgba(228, 231, 237, 0.6);
  position: sticky;
  top: 0;
  z-index: 50;
}

.header-inner {
  display: flex;
  align-items: center;
  height: $header-height;
  gap: 24px;
}

.logo {
  font-size: 20px;
  font-weight: 700;
  white-space: nowrap;
  background: $gradient-primary;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  transition: opacity $transition-fast;

  &:hover {
    opacity: 0.85;
  }
}

.nav-links {
  display: flex;
  gap: 4px;

  a {
    color: $text;
    font-size: 14px;
    padding: 6px 12px;
    border-radius: $radius-sm;
    position: relative;
    transition: all $transition-normal;

    &::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: 50%;
      width: 0;
      height: 2px;
      background: $gradient-primary;
      border-radius: 1px;
      transition: all $transition-normal;
      transform: translateX(-50%);
    }

    &:hover {
      color: $primary;

      &::after {
        width: 60%;
      }
    }

    &.router-link-active {
      color: $primary;

      &::after {
        width: 60%;
      }
    }
  }

  .mobile-user-section {
    display: none;
  }
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-left: auto;
}

.search-form {
  display: flex;
}

.search-input {
  width: 200px;
  padding: 7px 16px;
  border: 1px solid $border-light;
  border-radius: $radius-xl;
  font-size: 13px;
  outline: none;
  background: rgba(245, 247, 250, 0.8);
  transition: all $transition-normal;

  &:focus {
    border-color: $primary;
    width: 260px;
    box-shadow: 0 0 0 3px rgba(64, 158, 255, 0.15);
    background: $bg-white;
  }
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 12px;

  .username {
    font-size: 14px;
    font-weight: 500;
    color: $text;
  }

  .logout-link {
    color: $text-secondary;
    font-size: 14px;
    cursor: pointer;
    transition: color $transition-fast;

    &:hover {
      color: $primary;
    }
  }
}

.login-link {
  color: $text;
  font-size: 14px;
  padding: 6px 16px;
  border-radius: $radius-xl;
  transition: all $transition-normal;

  &:hover {
    color: #fff;
    background: $gradient-primary;
  }
}

.mobile-username {
  font-size: 14px;
  color: $text-secondary;
  padding: 4px 0;
}

// 移动端汉堡按钮 — 三条线变叉动画
.mobile-toggle {
  display: none;
  background: none;
  border: none;
  width: 28px;
  height: 20px;
  position: relative;
  cursor: pointer;

  span {
    display: block;
    position: absolute;
    width: 100%;
    height: 2px;
    background: $text;
    border-radius: 2px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

    &:nth-child(1) { top: 0; }
    &:nth-child(2) { top: 9px; }
    &:nth-child(3) { top: 18px; }
  }

  &.active span {
    &:nth-child(1) {
      top: 9px;
      transform: rotate(45deg);
    }
    &:nth-child(2) {
      opacity: 0;
    }
    &:nth-child(3) {
      top: 9px;
      transform: rotate(-45deg);
    }
  }
}

// 移动端适配
@media (max-width: 768px) {
  .nav-links {
    display: none;
    position: absolute;
    top: $header-height;
    left: 0;
    right: 0;
    background: $glass-bg;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(228, 231, 237, 0.6);
    flex-direction: column;
    padding: 16px 20px;
    gap: 4px;

    &.open {
      display: flex;
      animation: slideDown 0.3s ease;
    }

    a {
      padding: 10px 12px;

      &::after {
        display: none;
      }
    }

    .mobile-user-section {
      display: flex;
      flex-direction: column;
      gap: 8px;
      padding-top: 12px;
      border-top: 1px solid $border-light;
    }
  }

  .header-right {
    display: none;
  }

  .mobile-toggle {
    display: block;
  }
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
