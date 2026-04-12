<!-- 评论区组件：展示评论列表、发表评论、支持嵌套回复 -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { getComments, createComment } from '@/api/comments'
import type { Comment } from '@/types/comment'
import { formatDateTime } from '@/utils/format'

const props = defineProps<{
  articleId: number
}>()

const router = useRouter()
const authStore = useAuthStore()
const comments = ref<Comment[]>([])
const loading = ref(false)
const submitting = ref(false)
const submitError = ref('')  // 添加错误提示

// 评论表单字段
const content = ref('')
const nickname = ref('')
const email = ref('')
const replyTo = ref<number | null>(null)   // 正在回复的评论 ID

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
    await loadComments()         // 重新加载评论列表
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
        <div class="comment-header">
          <span class="comment-author">{{ comment.user?.username || comment.nickname || '游客' }}</span>
          <span class="comment-date">{{ formatDateTime(comment.created_at) }}</span>
        </div>
        <div class="comment-body">{{ comment.content }}</div>
        <button class="btn btn-sm reply-btn" @click="setReply(comment.id)">回复</button>
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
}

.comment-form {
  margin-bottom: 24px;

  textarea {
    width: 100%;
    padding: 12px;
    border: 1px solid $border;
    border-radius: 4px;
    font-size: 14px;
    resize: vertical;
    margin-bottom: 8px;
    outline: none;

    &:focus {
      border-color: $primary;
    }
  }
}

.reply-hint {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px;
  background: #ecf5ff;
  border-radius: 4px;
  margin-bottom: 8px;
  font-size: 13px;
  color: $primary;
}

.guest-fields {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;

  input {
    flex: 1;
    padding: 8px 12px;
    border: 1px solid $border;
    border-radius: 4px;
    font-size: 14px;
    outline: none;

    &:focus {
      border-color: $primary;
    }
  }
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.submit-error {
  color: #f56c6c;
  font-size: 13px;
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.comment-item {
  padding: 16px;
  border-radius: 8px;
  background: $bg-white;
  border: 1px solid $border-light;

  &.reply {
    margin-left: 24px;          // 回复项缩进
    background: $bg;
  }
}

.comment-header {
  display: flex;
  gap: 12px;
  margin-bottom: 8px;
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
}

.reply-btn {
  font-size: 12px;
}
</style>
