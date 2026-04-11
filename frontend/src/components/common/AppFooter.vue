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
  background: $bg-white;
  border-top: 1px solid $border-light;
  padding: 20px 0;
  text-align: center;
  color: $text-secondary;
  font-size: 14px;
}
</style>
