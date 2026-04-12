<!-- 管理后台布局：顶部栏 + 侧边导航 + 内容区 -->
<script setup lang="ts">
import { ref, computed } from 'vue'
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
      <button class="menu-toggle" @click="toggleSidebar">☰</button>
      <h1 class="admin-title">Jeffy Blog Admin</h1>
      <div class="header-right">
        <span class="username">{{ authStore.user?.username }}</span>
        <button class="btn btn-sm" @click="logout">退出登录</button>
        <router-link to="/" class="btn btn-sm">查看博客</router-link>
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
        <router-view />
      </main>
    </div>

    <!-- 移动端侧边栏遮罩 -->
    <div v-if="sidebarOpen" class="overlay" @click="sidebarOpen = false" />
  </div>
</template>

<style scoped lang="scss">
@use '@/assets/styles/variables' as *;

.admin-layout {
  min-height: 100vh;
}

.admin-header {
  height: $header-height;
  background: #304156;
  color: #fff;
  display: flex;
  align-items: center;
  padding: 0 20px;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
}

.menu-toggle {
  display: none;               // 桌面端隐藏，移动端显示
  background: none;
  border: none;
  color: #fff;
  font-size: 20px;
  cursor: pointer;
  margin-right: 16px;
}

.admin-title {
  font-size: 18px;
  font-weight: 600;
}

.header-right {
  margin-left: auto;           // 推到右侧
  display: flex;
  align-items: center;
  gap: 12px;

  .username {
    font-size: 14px;
  }

  .btn {
    color: #fff;
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.3);

    &:hover {
      background: rgba(255, 255, 255, 0.2);
      border-color: #fff;
    }
  }
}

.admin-body {
  display: flex;
  padding-top: $header-height; // 为固定顶栏留出空间
}

.sidebar {
  width: $sidebar-width;
  background: #fff;
  border-right: 1px solid $border-light;
  height: calc(100vh - #{$header-height});
  position: fixed;
  left: 0;
  top: $header-height;
  overflow-y: auto;
  z-index: 99;
}

.sidebar-nav {
  padding: 12px 0;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  color: $text;
  text-decoration: none;
  transition: all 0.2s;

  &:hover {
    background: $bg;
    color: $primary;
  }

  &.active {
    background: #ecf5ff;
    color: $primary;
    border-right: 3px solid $primary;  // 选中态右侧指示条
  }

  .nav-icon {
    margin-right: 12px;
    font-size: 16px;
  }
}

.admin-content {
  margin-left: $sidebar-width; // 为固定侧边栏留出空间
  flex: 1;
  padding: 24px;
  min-height: calc(100vh - #{$header-height});
}

.overlay {
  display: none;
}

// 移动端适配
@media (max-width: 768px) {
  .menu-toggle {
    display: block;            // 显示汉堡菜单按钮
  }

  .sidebar {
    transform: translateX(-100%); // 默认隐藏在左侧
    transition: transform 0.3s;

    &.open {
      transform: translateX(0);   // 展开时滑入
    }
  }

  .admin-content {
    margin-left: 0;            // 移动端去掉侧边栏占位
  }

  .overlay {
    display: block;
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.3);
    z-index: 98;
  }
}
</style>
