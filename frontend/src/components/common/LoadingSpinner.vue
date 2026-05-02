<!-- 加载提示组件 — 渐变旋转圆环 -->
<template>
  <div class="loading-spinner">
    <div class="spinner-ring"></div>
  </div>
</template>

<style scoped lang="scss">
@use '@/assets/styles/variables' as *;

.loading-spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px;
}

.spinner-ring {
  width: 32px;
  height: 32px;
  border: 3px solid $border-light;
  border-top-color: $primary;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
