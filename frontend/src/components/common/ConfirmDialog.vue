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
    <div v-if="visible" class="confirm-overlay" @click.self="emit('cancel')">
      <div class="confirm-dialog">
        <h3 class="confirm-title">{{ title }}</h3>
        <p class="confirm-message">{{ message }}</p>
        <div class="confirm-actions">
          <button class="btn" @click="emit('cancel')">Cancel</button>
          <button class="btn btn-danger" @click="emit('confirm')">Confirm</button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped lang="scss">
@use '@/assets/styles/variables' as *;

.confirm-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5); // 半透明遮罩
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 200;
}

.confirm-dialog {
  background: $bg-white;
  border-radius: 8px;
  padding: 24px;
  max-width: 400px;
  width: 90%;
}

.confirm-title {
  font-size: 18px;
  margin-bottom: 12px;
}

.confirm-message {
  color: $text-secondary;
  margin-bottom: 24px;
}

.confirm-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}
</style>
