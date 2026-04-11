<!-- 点赞按钮组件：支持点赞/取消点赞，未登录时跳转登录页 -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api'

const props = defineProps<{
  articleId: number    // 文章 ID
  likeCount: number    // 初始点赞数
}>()

const router = useRouter()
const authStore = useAuthStore()
const liked = ref(false)
const count = ref(props.likeCount)

onMounted(async () => {
  // 已登录时查询当前用户是否已点赞
  if (authStore.isLoggedIn) {
    try {
      const { data } = await api.get(`/articles/${props.articleId}/liked`)
      liked.value = data.liked
    } catch { /* ignore */ }
  }
})

/** 切换点赞状态 */
async function toggleLike() {
  if (!authStore.isLoggedIn) {
    router.push('/login')
    return
  }
  try {
    const { data } = await api.post(`/articles/${props.articleId}/like`)
    liked.value = data.liked
    count.value += data.liked ? 1 : -1  // 根据返回状态增减计数
  } catch { /* ignore */ }
}
</script>

<template>
  <button class="like-btn" :class="{ liked }" @click="toggleLike">
    {{ liked ? '❤️' : '🤍' }} {{ count }}
  </button>
</template>

<style scoped lang="scss">
@use '@/assets/styles/variables' as *;

.like-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border: 1px solid $border;
  border-radius: 20px;
  background: $bg-white;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;

  &:hover {
    border-color: $danger;
  }

  &.liked {
    border-color: $danger;
    background: #fef0f0;         // 已点赞时浅红背景
  }
}
</style>
