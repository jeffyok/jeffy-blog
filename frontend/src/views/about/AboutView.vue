<!-- 关于页面 -->
<template>
  <div>
    <h1 class="page-title">关于</h1>
    <div class="card about-content">
      <p>欢迎来到 Jeffy Blog。这是一个使用 FastAPI、Vue 3 和 MySQL 构建的个人博客。</p>
      <p>欢迎浏览文章、发表评论，并通过 RSS 订阅更新。</p>
    </div>
  </div>
</template>

<style scoped lang="scss">
@use '@/assets/styles/variables' as *;

.about-content {
  position: relative;
  overflow: hidden;

  // 顶部渐变装饰条
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: $gradient-primary;
  }

  p {
    line-height: 1.8;
    color: $text;
    font-size: 15px;

    & + p {
      margin-top: 12px;
    }
  }
}
</style>
