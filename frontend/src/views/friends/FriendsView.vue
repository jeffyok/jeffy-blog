<!-- 友情链接页面：网格展示所有友情链接 -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getFriendLinks } from '@/api/friendLinks'
import type { FriendLink } from '@/types/api'

const links = ref<FriendLink[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const { data } = await getFriendLinks()
    links.value = data
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div>
    <h1 class="page-title">友情链接</h1>
    <div v-if="loading" class="loading"><span>加载中...</span></div>
    <div v-else-if="links.length === 0" class="empty">暂无友情链接。</div>
    <!-- 友链网格 -->
    <div v-else class="friends-grid">
      <a v-for="link in links" :key="link.id" :href="link.url" target="_blank" rel="noopener" class="card friend-card">
        <div v-if="link.logo" class="friend-logo">
          <img :src="link.logo" :alt="link.title" />
        </div>
        <div class="friend-info">
          <h3 class="friend-title">{{ link.title }}</h3>
          <p v-if="link.description" class="friend-desc">{{ link.description }}</p>
        </div>
      </a>
    </div>
  </div>
</template>

<style scoped lang="scss">
@use '@/assets/styles/variables' as *;

.friends-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.friend-card {
  display: flex;
  align-items: center;
  gap: 14px;
  text-decoration: none;
  color: $text;
  position: relative;
  overflow: hidden;

  // 渐变边框效果
  &::after {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: $radius-lg;
    padding: 1px;
    background: $gradient-card-border;
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    opacity: 0;
    transition: opacity $transition-normal;
  }

  &:hover {
    transform: translateY(-3px);
    box-shadow: $shadow-lg;

    &::after {
      opacity: 1;
    }

    .friend-logo {
      box-shadow: 0 0 0 3px rgba(64, 158, 255, 0.2);
    }
  }
}

.friend-logo {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
  transition: box-shadow $transition-normal;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

.friend-info {
  min-width: 0;
}

.friend-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 4px;
  transition: color $transition-fast;

  .friend-card:hover & {
    color: $primary;
  }
}

.friend-desc {
  font-size: 13px;
  color: $text-secondary;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
