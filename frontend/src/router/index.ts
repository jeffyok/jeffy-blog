/**
 * 路由配置
 * 定义前台页面、后台管理页面路由及导航守卫
 */
import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('@/layouts/DefaultLayout.vue'),
    children: [
      { path: '', name: 'home', component: () => import('@/views/home/HomeView.vue') },
      { path: 'article/:slug', name: 'article-detail', component: () => import('@/views/article/ArticleDetailView.vue') },
      { path: 'category/:slug', name: 'category', component: () => import('@/views/category/CategoryView.vue') },
      { path: 'tag/:slug', name: 'tag', component: () => import('@/views/tag/TagView.vue') },
      { path: 'archive', name: 'archive', component: () => import('@/views/archive/ArchiveView.vue') },
      { path: 'search', name: 'search', component: () => import('@/views/search/SearchView.vue') },
      { path: 'about', name: 'about', component: () => import('@/views/about/AboutView.vue') },
      { path: 'login', name: 'login', component: () => import('@/views/auth/LoginView.vue') },
      { path: 'register', name: 'register', component: () => import('@/views/auth/RegisterView.vue') },
      { path: 'friends', name: 'friend-links', component: () => import('@/views/friends/FriendsView.vue') },
    ],
  },
  {
    path: '/admin',
    component: () => import('@/layouts/AdminLayout.vue'),
    // 标记需要管理员权限
    meta: { requiresAdmin: true },
    children: [
      { path: '', name: 'admin-dashboard', component: () => import('@/views/admin/DashboardView.vue') },
      { path: 'articles', name: 'admin-articles', component: () => import('@/views/admin/ArticleListView.vue') },
      { path: 'articles/new', name: 'admin-article-new', component: () => import('@/views/admin/ArticleEditorView.vue') },
      { path: 'articles/:id/edit', name: 'admin-article-edit', component: () => import('@/views/admin/ArticleEditorView.vue') },
      { path: 'categories', name: 'admin-categories', component: () => import('@/views/admin/CategoryManageView.vue') },
      { path: 'tags', name: 'admin-tags', component: () => import('@/views/admin/TagManageView.vue') },
      { path: 'comments', name: 'admin-comments', component: () => import('@/views/admin/CommentManageView.vue') },
      { path: 'users', name: 'admin-users', component: () => import('@/views/admin/UserManageView.vue') },
    ],
  },
  // 404 兜底路由
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/views/NotFoundView.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  // 路由切换时滚动到顶部
  scrollBehavior() {
    return { top: 0 }
  },
})

// 全局前置守卫：恢复用户信息 + 管理员权限校验
router.beforeEach(async (to) => {
  const authStore = useAuthStore()
  // 有 token 但未加载用户信息时自动获取
  if (authStore.token && !authStore.user) {
    await authStore.fetchUser()
  }
  // 非管理员访问后台页面时重定向到登录
  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    return '/login'
  }
})

export default router
