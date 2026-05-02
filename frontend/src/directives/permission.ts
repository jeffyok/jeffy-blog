/**
 * v-permission 自定义指令
 * 根据用户权限控制元素显示/隐藏
 *
 * 用法：
 *   v-permission="'articles:create'"  — 需要特定权限
 *   v-permission="['articles:create', 'articles:edit']"  — 满足任一即可
 */
import type { Directive, DirectiveBinding } from 'vue'

function checkPermission(_el: HTMLElement, binding: DirectiveBinding<string | string[]>, authStore: any): boolean {
  const store = authStore()
  const value = binding.value
  if (typeof value === 'string') {
    return store.hasPermission(value)
  }
  if (Array.isArray(value)) {
    return store.hasAnyPermission(...value)
  }
  return false
}

export const permission: Directive = {
  mounted(el: HTMLElement, binding: DirectiveBinding<string | string[]>) {
    // 动态导入 store 避免循环依赖
    import('@/stores/auth').then(({ useAuthStore }) => {
      const has = checkPermission(el, binding, useAuthStore)
      if (!has) {
        el.parentNode?.removeChild(el)
      }
    })
  },
  updated(el: HTMLElement, binding: DirectiveBinding<string | string[]>) {
    import('@/stores/auth').then(({ useAuthStore }) => {
      const has = checkPermission(el, binding, useAuthStore)
      if (!has) {
        el.parentNode?.removeChild(el)
      }
    })
  },
}
