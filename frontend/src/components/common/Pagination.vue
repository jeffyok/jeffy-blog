<!-- 分页组件：显示页码按钮，支持上一页/下一页 -->
<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  total: number       // 数据总条数
  page: number        // 当前页码
  pageSize: number    // 每页条数
}>()

const emit = defineEmits<{
  'update:page': [page: number]
}>()

// 计算总页数
const totalPages = computed(() => Math.ceil(props.total / props.pageSize))

/** 跳转到指定页码 */
function goTo(page: number) {
  if (page >= 1 && page <= totalPages.value) {
    emit('update:page', page)
  }
}
</script>

<template>
  <div v-if="totalPages > 1" class="pagination">
    <!-- 上一页 -->
    <button
      class="page-btn"
      :class="{ disabled: page <= 1 }"
      @click="goTo(page - 1)"
    >
      &lt;
    </button>
    <!-- 页码按钮 -->
    <button
      v-for="p in totalPages"
      :key="p"
      class="page-btn"
      :class="{ active: p === page }"
      @click="goTo(p)"
    >
      {{ p }}
    </button>
    <!-- 下一页 -->
    <button
      class="page-btn"
      :class="{ disabled: page >= totalPages }"
      @click="goTo(page + 1)"
    >
      &gt;
    </button>
  </div>
</template>

<style scoped lang="scss">
@use '@/assets/styles/variables' as *;

.pagination {
  display: flex;
  gap: 8px;
  justify-content: center;
  margin-top: 16px;
}

.page-btn {
  min-width: 36px;
  height: 36px;
  padding: 0 8px;
  border: 1px solid $border;
  background: $bg-white;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;

  &:hover:not(.disabled):not(.active) {
    border-color: $primary;
    color: $primary;
  }

  &.active {
    background: $primary;
    color: white;
    border-color: $primary;
  }

  &.disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }
}
</style>
