<!-- 404 页面：路由未匹配时显示 -->
<template>
  <div class="not-found">
    <h1>404</h1>
    <p>Page not found.</p>
    <router-link to="/" class="btn btn-primary">Back to Home</router-link>
  </div>
</template>

<style scoped lang="scss">
.not-found {
  text-align: center;
  padding: 80px 0;

  h1 {
    font-size: 72px;
    color: #c0c4cc;
    margin-bottom: 16px;
  }

  p {
    font-size: 18px;
    color: #909399;
    margin-bottom: 24px;
  }
}
</style>
