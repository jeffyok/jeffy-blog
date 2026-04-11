<!-- 前台顶部导航栏：Logo + 导航链接 + 搜索框 + 移动端菜单 -->
<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const mobileMenuOpen = ref(false)
const searchKeyword = ref('')

/** 提交搜索，跳转到搜索页面 */
function handleSearch() {
  if (searchKeyword.value.trim()) {
    router.push({ name: 'search', query: { q: searchKeyword.value.trim() } })
    searchKeyword.value = ''
    mobileMenuOpen = false
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
        <router-link to="/" @click="mobileMenuOpen = false">Home</router-link>
        <router-link to="/archive" @click="mobileMenuOpen = false">Archive</router-link>
        <router-link to="/friends" @click="mobileMenuOpen = false">Friends</router-link>
        <router-link to="/about" @click="mobileMenuOpen = false">About</router-link>
        <!-- 仅管理员可见的后台入口 -->
        <template v-if="authStore.isAdmin">
          <router-link to="/admin" @click="mobileMenuOpen = false">Admin</router-link>
        </template>
        <!-- 已登录显示退出，未登录显示登录 -->
        <template v-if="authStore.isLoggedIn">
          <a href="#" @click.prevent="logout">Logout</a>
        </template>
        <template v-else>
          <router-link to="/login" @click="mobileMenuOpen = false">Login</router-link>
        </template>
      </nav>
      <!-- 搜索表单 -->
      <form class="search-form" @submit.prevent="handleSearch">
        <input v-model="searchKeyword" type="text" placeholder="Search..." class="search-input" />
      </form>
      <!-- 移动端汉堡菜单按钮 -->
      <button class="mobile-toggle" @click="mobileMenuOpen = !mobileMenuOpen">☰</button>
    </div>
  </header>
</template>

<style scoped lang="scss">
@use '@/assets/styles/variables' as *;

.app-header {
  background: $bg-white;
  border-bottom: 1px solid $border-light;
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
  color: $text;
  white-space: nowrap;

  &:hover {
    color: $primary;
  }
}

.nav-links {
  display: flex;
  gap: 16px;

  a {
    color: $text;
    font-size: 14px;
    padding: 4px 0;
    transition: color 0.2s;

    &:hover, &.router-link-active {
      color: $primary;
    }
  }
}

.search-form {
  margin-left: auto;           // 搜索框推到右侧
  display: flex;
}

.search-input {
  width: 200px;
  padding: 6px 12px;
  border: 1px solid $border;
  border-radius: 20px;
  font-size: 13px;
  outline: none;

  &:focus {
    border-color: $primary;
    width: 260px;              // 聚焦时展宽
  }
}

.mobile-toggle {
  display: none;               // 桌面端隐藏
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
}

// 移动端适配
@media (max-width: 768px) {
  .nav-links {
    display: none;             // 默认隐藏
    position: absolute;
    top: $header-height;
    left: 0;
    right: 0;
    background: $bg-white;
    border-bottom: 1px solid $border-light;
    flex-direction: column;
    padding: 12px 20px;
    gap: 8px;

    &.open {
      display: flex;           // 展开时显示
    }
  }

  .search-form {
    display: none;             // 移动端隐藏搜索框
  }

  .mobile-toggle {
    display: block;
  }
}
</style>
