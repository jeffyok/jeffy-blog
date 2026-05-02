<!-- 评论区组件：展示评论列表、发表评论、支持嵌套回复 -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { getComments, createComment } from '@/api/comments'
import type { Comment } from '@/types/comment'
import { formatDateTime } from '@/utils/format'

const props = defineProps<{
  articleId: number
}>()

const authStore = useAuthStore()
const comments = ref<Comment[]>([])
const loading = ref(false)
const submitting = ref(false)
const submitError = ref('')

// 评论表单字段
const content = ref('')
const nickname = ref('')
const email = ref('')
const replyTo = ref<number | null>(null)

onMounted(loadComments)

/** 加载评论列表 */
async function loadComments() {
  loading.value = true
  try {
    const { data } = await getComments(props.articleId)
    comments.value = data
  } catch (e) {
    console.error('加载评论失败:', e)
  } finally {
    loading.value = false
  }
}

/** 设置回复目标 */
function setReply(commentId: number) {
  replyTo.value = commentId
}

/** 取消回复 */
function cancelReply() {
  replyTo.value = null
}

/** 提交评论 */
async function submitComment() {
  if (!content.value.trim()) return
  if (!authStore.isLoggedIn && (!nickname.value || !email.value)) return

  submitting.value = true
  submitError.value = ''
  try {
    await createComment(props.articleId, {
      content: content.value.trim(),
      parent_id: replyTo.value || undefined,
      nickname: nickname.value || undefined,
      email: email.value || undefined,
    })
    content.value = ''
    replyTo.value = null
    try {
      await loadComments()
    } catch (e) {
      console.error('加载评论列表失败:', e)
    }
  } catch (e) {
    console.error('提交评论失败:', e)
    submitError.value = '提交评论失败，请稍后重试'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="comment-section">
    <h2 class="section-title">评论</h2>

    <!-- 评论输入表单 -->
    <div class="comment-form card">
      <textarea v-model="content" placeholder="写下你的评论..." rows="3" />
      <!-- 回复提示 -->
      <div v-if="replyTo" class="reply-hint">
        正在回复评论 #{{ replyTo }}
        <button class="btn btn-sm" @click="cancelReply">取消</button>
      </div>
      <!-- 未登录时显示昵称和邮箱输入框 -->
      <div v-if="!authStore.isLoggedIn" class="guest-fields">
        <input v-model="nickname" placeholder="昵称" required />
        <input v-model="email" type="email" placeholder="邮箱" required />
      </div>
      <div class="form-actions">
        <!-- 错误提示 -->
        <div v-if="submitError" class="submit-error">{{ submitError }}</div>
        <button class="btn btn-primary" @click="submitComment" :disabled="submitting || !content.trim()">
          {{ submitting ? '提交中...' : '提交评论' }}
        </button>
      </div>
    </div>

    <!-- 加载中 / 空状态 -->
    <div v-if="loading" class="loading"><span>加载中...</span></div>
    <div v-else-if="comments.length === 0" class="empty">暂无评论。</div>

    <!-- 评论列表 -->
    <div v-else class="comment-list">
      <div v-for="comment in comments" :key="comment.id" class="comment-item">
        <div class="comment-avatar">{{ (comment.user?.username || comment.nickname || '游')[0] }}</div>
        <div class="comment-body-wrap">
          <div class="comment-header">
            <span class="comment-author">{{ comment.user?.username || comment.nickname || '游客' }}</span>
            <span class="comment-date">{{ formatDateTime(comment.created_at) }}</span>
          </div>
          <div class="comment-body">{{ comment.content }}</div>
          <button class="reply-btn" @click="setReply(comment.id)">回复</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@use '@/assets/styles/variables' as *;

.comment-section {
  margin-top: 32px;
}

.section-title {
  font-size: 20px;
  margin-bottom: 16px;
  font-weight: 600;
  padding-left: 16px;
  position: relative;

  &::before {
    content: '';
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 4px;
    height: 20px;
    border-radius: 2px;
    background: $gradient-primary;
  }
}

.comment-form {
  margin-bottom: 24px;

  textarea {
    width: 100%;
    padding: 12px 16px;
    border: 1px solid $border;
    border-radius: $radius-sm;
    font-size: 14px;
    resize: vertical;
    margin-bottom: 8px;
    outline: none;
    transition: all $transition-normal;
    background: $bg-white;

    &:focus {
      border-color: $primary;
      box-shadow: 0 0 0 3px rgba(64, 158, 255, 0.15);
    }
  }
}

.reply-hint {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: rgba(64, 158, 255, 0.06);
  border-radius: $radius-sm;
  margin-bottom: 8px;
  font-size: 13px;
  color: $primary;
  border-left: 3px solid $primary;
}

.guest-fields {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;

  input {
    flex: 1;
    padding: 10px 14px;
    border: 1px solid $border;
    border-radius: $radius-sm;
    font-size: 14px;
    outline: none;
    transition: all $transition-normal;

    &:focus {
      border-color: $primary;
      box-shadow: 0 0 0 3px rgba(64, 158, 255, 0.15);
    }
  }
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 12px;
}

.submit-error {
  color: $danger;
  font-size: 13px;
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.comment-item {
  display: flex;
  gap: 12px;
  padding: 16px;
  border-radius: $radius-md;
  background: $glass-card-bg;
  backdrop-filter: blur(8px);
  border: 1px solid $glass-border;
  transition: all $transition-normal;

  &:hover {
    border-color: rgba(64, 158, 255, 0.15);
    box-shadow: $shadow-sm;
  }

  &.reply {
    margin-left: 48px;
    background: rgba(245, 247, 250, 0.6);
  }
}

.comment-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: $gradient-primary;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
  flex-shrink: 0;
}

.comment-body-wrap {
  flex: 1;
  min-width: 0;
}

.comment-header {
  display: flex;
  gap: 12px;
  margin-bottom: 6px;
  font-size: 13px;
}

.comment-author {
  font-weight: 600;
  color: $text;
}

.comment-date {
  color: $text-secondary;
}

.comment-body {
  color: $text;
  line-height: 1.6;
  margin-bottom: 8px;
  font-size: 14px;
}

.reply-btn {
  background: none;
  border: none;
  color: $text-secondary;
  font-size: 12px;
  cursor: pointer;
  padding: 2px 8px;
  border-radius: $radius-sm;
  transition: all $transition-fast;

  &:hover {
    color: $primary;
    background: rgba(64, 158, 255, 0.06);
  }
}
</style>
