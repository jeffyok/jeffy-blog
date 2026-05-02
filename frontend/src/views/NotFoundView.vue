<!-- 404 页面：路由未匹配时显示 -->
<template>
  <div class="not-found">
    <h1 class="code">404</h1>
    <p class="message">页面未找到</p>
    <router-link to="/" class="btn btn-primary back-btn">返回首页</router-link>
  </div>
</template>

<style scoped lang="scss">
@use '@/assets/styles/variables' as *;

.not-found {
  text-align: center;
  padding: 80px 0;
}

.code {
  font-size: 96px;
  font-weight: 800;
  background: $gradient-primary;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 8px;
  animation: float 3s ease-in-out infinite;
  line-height: 1.2;
}

.message {
  font-size: 18px;
  color: $text-secondary;
  margin-bottom: 32px;
}

.back-btn {
  padding: 10px 28px;
  font-size: 15px;
  border-radius: $radius-xl;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-12px); }
}
</style>
