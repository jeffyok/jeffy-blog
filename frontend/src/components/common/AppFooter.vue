<!-- 前台底部栏 -->
<template>
  <footer class="app-footer">
    <div class="container footer-inner">
      <p>&copy; {{ new Date().getFullYear() }} Jeffy Blog. All rights reserved.</p>
    </div>
  </footer>
</template>

<style scoped lang="scss">
@use '@/assets/styles/variables' as *;

.app-footer {
  background: $glass-bg;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  padding: 20px 0;
  text-align: center;
  color: $text-secondary;
  font-size: 14px;
  position: relative;

  // 顶部渐变分割线
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: $gradient-card-border;
  }
}
</style>
