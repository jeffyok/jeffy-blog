<!-- 点赞按钮组件：支持点赞/取消点赞，未登录时跳转登录页 -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api'

const props = defineProps<{
  articleId: number
  likeCount: number
}>()

const router = useRouter()
const authStore = useAuthStore()
const liked = ref(false)
const count = ref(props.likeCount)

onMounted(async () => {
  if (authStore.isLoggedIn) {
    try {
      const { data } = await api.get(`/articles/${props.articleId}/liked/`)
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
    const { data } = await api.post(`/articles/${props.articleId}/like/`)
    liked.value = data.liked
    count.value += data.liked ? 1 : -1
  } catch { /* ignore */ }
}
</script>

<template>
  <button class="like-btn" :class="{ liked }" @click="toggleLike">
    <span class="like-icon">{{ liked ? '❤️' : '🤍' }}</span>
    {{ count }}
  </button>
</template>

<style scoped lang="scss">
@use '@/assets/styles/variables' as *;

.like-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 20px;
  border: 1px solid $border;
  border-radius: $radius-xl;
  background: $glass-bg;
  backdrop-filter: blur(8px);
  cursor: pointer;
  font-size: 14px;
  transition: all $transition-normal;

  &:hover {
    border-color: $danger;
    box-shadow: $shadow-sm;

    .like-icon {
      animation: heartbeat 0.6s ease-in-out;
    }
  }

  &.liked {
    border-color: $danger;
    background: linear-gradient(135deg, rgba(245, 108, 108, 0.08) 0%, rgba(230, 71, 91, 0.08) 100%);
    color: $danger;
    box-shadow: 0 2px 8px rgba(245, 108, 108, 0.2);
  }
}

.like-icon {
  display: inline-block;
}

@keyframes heartbeat {
  0% { transform: scale(1); }
  25% { transform: scale(1.3); }
  50% { transform: scale(1); }
  75% { transform: scale(1.15); }
  100% { transform: scale(1); }
}
</style>
