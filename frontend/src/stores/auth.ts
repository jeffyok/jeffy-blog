/**
 * 认证状态管理
 * 管理用户登录态、token、用户信息
 */
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import type { User } from '@/types/user'
import * as authApi from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  // 从 localStorage 恢复 token，保持刷新后登录态
  const token = ref(localStorage.getItem('token') || '')

  /** 是否已登录 */
  const isLoggedIn = computed(() => !!token.value)
  /** 是否为管理员 */
  const isAdmin = computed(() => user.value?.role === 'admin')

  /** 登录并获取用户信息 */
  async function login(username: string, password: string) {
    const { data } = await authApi.login(username, password)
    token.value = data.access_token
    localStorage.setItem('token', data.access_token)
    await fetchUser()
  }

  /** 注册新用户 */
  async function register(username: string, email: string, password: string) {
    await authApi.register(username, email, password)
  }

  /** 根据 token 获取当前用户信息 */
  async function fetchUser() {
    try {
      const { data } = await authApi.getMe()
      user.value = data
    } catch {
      // token 无效时清除登录态
      logout()
    }
  }

  /** 退出登录 */
  function logout() {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
  }

  return { user, token, isLoggedIn, isAdmin, login, register, fetchUser, logout }
})
