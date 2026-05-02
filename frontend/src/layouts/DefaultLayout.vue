<!-- 前台默认布局：顶部导航 + 主内容区 + 底部 -->
<script setup lang="ts">
import AppHeader from '@/components/common/AppHeader.vue'
import AppFooter from '@/components/common/AppFooter.vue'
</script>

<template>
  <div class="default-layout">
    <AppHeader />
    <main class="main-content">
      <div class="container">
        <router-view v-slot="{ Component }">
          <Transition name="page-fade" mode="out-in">
            <component :is="Component" />
          </Transition>
        </router-view>
      </div>
    </main>
    <AppFooter />
  </div>
</template>

<style scoped lang="scss">
@use '@/assets/styles/variables' as *;

.default-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding: 24px 0;
}
</style>
