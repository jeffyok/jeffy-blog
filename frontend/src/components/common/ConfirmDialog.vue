<!-- 确认对话框：通过 Teleport 挂载到 body，用于删除等危险操作的二次确认 -->
<script setup lang="ts">
defineProps<{
  visible: boolean   // 是否显示
  title: string      // 标题
  message: string    // 提示信息
}>()

const emit = defineEmits<{
  confirm: []        // 确认事件
  cancel: []         // 取消事件
}>()
</script>

<template>
  <Teleport to="body">
    <!-- 点击遮罩层可取消 -->
    <Transition name="dialog">
      <div v-if="visible" class="confirm-overlay" @click.self="emit('cancel')">
        <div class="confirm-dialog">
          <h3 class="confirm-title">{{ title }}</h3>
          <p class="confirm-message">{{ message }}</p>
          <div class="confirm-actions">
            <button class="btn" @click="emit('cancel')">取消</button>
            <button class="btn btn-danger" @click="emit('confirm')">确认</button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped lang="scss">
@use '@/assets/styles/variables' as *;

.confirm-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 200;
}

.confirm-dialog {
  background: $bg-white;
  border-radius: $radius-lg;
  padding: 28px;
  max-width: 400px;
  width: 90%;
  box-shadow: $shadow-xl;
}

.confirm-title {
  font-size: 18px;
  margin-bottom: 12px;
  font-weight: 600;
}

.confirm-message {
  color: $text-secondary;
  margin-bottom: 24px;
  line-height: 1.6;
}

.confirm-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

// 弹窗过渡动画
.dialog-enter-active {
  transition: all 0.3s $ease-out-back;

  .confirm-dialog {
    animation: dialogEnter 0.3s $ease-out-back;
  }
}

.dialog-leave-active {
  transition: all 0.2s ease-in;
}

.dialog-enter-from {
  opacity: 0;

  .confirm-dialog {
    transform: scale(0.9);
  }
}

.dialog-leave-to {
  opacity: 0;
}

@keyframes dialogEnter {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}
</style>
