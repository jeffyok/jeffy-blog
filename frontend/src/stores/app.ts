/**
 * 应用全局状态管理
 * 管理侧边栏和搜索等全局 UI 状态
 */
import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', () => {
  const sidebarOpen = ref(false)
  const searchKeyword = ref('')

  /** 切换侧边栏展开/收起 */
  function toggleSidebar() {
    sidebarOpen.value = !sidebarOpen.value
  }

  /** 关闭侧边栏 */
  function closeSidebar() {
    sidebarOpen.value = false
  }

  return { sidebarOpen, searchKeyword, toggleSidebar, closeSidebar }
})
