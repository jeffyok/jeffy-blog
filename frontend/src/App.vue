<!-- 根组件：渲染路由视图，并在挂载时初始化用户信息 -->
<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

/** 应用挂载后，如果有 token 则自动获取用户信息 */
onMounted(async () => {
  if (authStore.token) {
    await authStore.fetchUser()
  }
})
</script>

<template>
  <router-view />
</template>
