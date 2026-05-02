<!-- 管理后台布局：顶部栏 + 侧边导航 + 内容区 -->
<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const sidebarOpen = ref(false)

// 侧边栏菜单项
const menuItems = [
  { name: '仪表盘', path: '/admin', icon: '📊' },
  { name: '文章管理', path: '/admin/articles', icon: '📝', matchPrefix: true },
  { name: '分类管理', path: '/admin/categories', icon: '📂' },
  { name: '标签管理', path: '/admin/tags', icon: '🏷️' },
  { name: '评论管理', path: '/admin/comments', icon: '💬' },
  { name: '用户管理', path: '/admin/users', icon: '👥' },
]

/** 判断菜单项是否激活 */
function isActive(item: { path: string; matchPrefix?: boolean }) {
  if (item.matchPrefix) {
    return route.path.startsWith(item.path)
  }
  return route.path === item.path
}

/** 切换侧边栏展开/收起 */
function toggleSidebar() {
  sidebarOpen.value = !sidebarOpen.value
}

/** 退出登录并跳转登录页 */
function logout() {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <div class="admin-layout">
    <!-- 顶部栏 -->
    <header class="admin-header">
      <button class="menu-toggle" @click="toggleSidebar">
        <span></span>
        <span></span>
        <span></span>
      </button>
      <h1 class="admin-title">Jeffy Blog Admin</h1>
      <div class="header-right">
        <span class="username">{{ authStore.user?.username }}</span>
        <button class="btn btn-sm header-btn" @click="logout">退出登录</button>
        <router-link to="/" class="btn btn-sm header-btn">查看博客</router-link>
      </div>
    </header>

    <div class="admin-body">
      <!-- 侧边导航 -->
      <aside class="sidebar" :class="{ open: sidebarOpen }">
        <nav class="sidebar-nav">
          <router-link
            v-for="item in menuItems"
            :key="item.path"
            :to="item.path"
            class="nav-item"
            :class="{ active: isActive(item) }"
            @click="sidebarOpen = false"
          >
            <span class="nav-icon">{{ item.icon }}</span>
            <span>{{ item.name }}</span>
          </router-link>
        </nav>
      </aside>

      <!-- 主内容区 -->
      <main class="admin-content">
        <router-view v-slot="{ Component }">
          <Transition name="page-fade" mode="out-in">
            <component :is="Component" />
          </Transition>
        </router-view>
      </main>
    </div>

    <!-- 移动端侧边栏遮罩 -->
    <Transition name="fade">
      <div v-if="sidebarOpen" class="overlay" @click="sidebarOpen = false" />
    </Transition>
  </div>
</template>

<style scoped lang="scss">
@use '@/assets/styles/variables' as *;

.admin-layout {
  min-height: 100vh;
}

.admin-header {
  height: $header-height;
  background: linear-gradient(135deg, #1a2332 0%, #2d3a4a 100%);
  backdrop-filter: blur(12px);
  color: #fff;
  display: flex;
  align-items: center;
  padding: 0 20px;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
}

.menu-toggle {
  display: none;
  background: none;
  border: none;
  width: 28px;
  height: 20px;
  position: relative;
  cursor: pointer;
  margin-right: 16px;

  span {
    display: block;
    position: absolute;
    width: 100%;
    height: 2px;
    background: #fff;
    border-radius: 2px;
    transition: all 0.3s ease;

    &:nth-child(1) { top: 0; }
    &:nth-child(2) { top: 9px; }
    &:nth-child(3) { top: 18px; }
  }
}

.admin-title {
  font-size: 18px;
  font-weight: 600;
  background: linear-gradient(135deg, #66b1ff, #a78bfa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.header-right {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 12px;

  .username {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.8);
  }

  .header-btn {
    color: #fff;
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(8px);

    &:hover {
      background: rgba(255, 255, 255, 0.15);
      border-color: rgba(255, 255, 255, 0.4);
    }
  }
}

.admin-body {
  display: flex;
  padding-top: $header-height;
}

.sidebar {
  width: $sidebar-width;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-right: 1px solid $border-light;
  height: calc(100vh - #{$header-height});
  position: fixed;
  left: 0;
  top: $header-height;
  overflow-y: auto;
  z-index: 99;
}

.sidebar-nav {
  padding: 16px 0;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  color: $text;
  text-decoration: none;
  transition: all $transition-normal;
  position: relative;
  margin: 2px 8px;
  border-radius: $radius-sm;

  &:hover {
    background: rgba(64, 158, 255, 0.06);
    color: $primary;
  }

  &.active {
    background: rgba(64, 158, 255, 0.1);
    color: $primary;
    font-weight: 500;

    // 左侧渐变条
    &::before {
      content: '';
      position: absolute;
      left: -8px;
      top: 50%;
      transform: translateY(-50%);
      width: 3px;
      height: 60%;
      border-radius: 2px;
      background: $gradient-primary;
    }
  }

  .nav-icon {
    margin-right: 12px;
    font-size: 16px;
  }
}

.admin-content {
  margin-left: $sidebar-width;
  flex: 1;
  padding: 24px;
  min-height: calc(100vh - #{$header-height});
  background: $bg;
}

.overlay {
  display: none;
}

// 移动端适配
@media (max-width: 768px) {
  .menu-toggle {
    display: block;
  }

  .sidebar {
    transform: translateX(-100%);
    transition: transform 0.3s $ease-smooth;

    &.open {
      transform: translateX(0);
    }
  }

  .admin-content {
    margin-left: 0;
  }

  .overlay {
    display: block;
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(4px);
    z-index: 98;
  }
}

// 遮罩层过渡
.fade-enter-active { transition: opacity 0.2s ease; }
.fade-leave-active { transition: opacity 0.15s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>
