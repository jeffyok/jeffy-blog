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
    <h1 class="page-title">Friend Links</h1>
    <div v-if="loading" class="loading"><span>Loading...</span></div>
    <div v-else-if="links.length === 0" class="empty">No friend links yet.</div>
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
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); // 自适应列数
  gap: 16px;
}

.friend-card {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: $text;
  transition: box-shadow 0.2s, transform 0.2s;

  &:hover {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    transform: translateY(-2px);
  }
}

.friend-logo {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

.friend-info {
  min-width: 0;                  // 允许文本溢出省略
}

.friend-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 4px;
}

.friend-desc {
  font-size: 13px;
  color: $text-secondary;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
