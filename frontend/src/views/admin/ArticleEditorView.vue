<!-- 文章编辑器页面：新建/编辑文章，Markdown 编辑 + 右侧元数据面板 -->
<script setup lang="ts">
import { ref, onMounted, computed, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { MdEditor } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import { getArticleById, createArticle, updateArticle } from '@/api/articles'
import { getCategories } from '@/api/categories'
import { getTags } from '@/api/tags'
import type { Category, Tag } from '@/types/article'

const route = useRoute()
const router = useRouter()
const isEdit = computed(() => !!route.params.id)
const loading = ref(true)
const saving = ref(false)
const saveError = ref('')

const form = ref({
  title: '',
  slug: '',
  content: '',
  summary: '',
  cover_image: '',
  category_id: undefined as number | undefined,
  tag_ids: [] as number[],
  status: 'draft',
  is_top: false,
})

const categories = ref<Category[]>([])
const tags = ref<Tag[]>([])

let autoSaveTimer: ReturnType<typeof setTimeout> | null = null

onMounted(async () => {
  await Promise.all([loadCategories(), loadTags()])
  if (isEdit.value) {
    await loadArticle()
  }
  loading.value = false
})

onBeforeUnmount(() => {
  if (autoSaveTimer) clearTimeout(autoSaveTimer)
})

async function loadCategories() {
  try {
    const { data } = await getCategories()
    categories.value = data
  } catch { /* ignore */ }
}

async function loadTags() {
  try {
    const { data } = await getTags()
    tags.value = data
  } catch { /* ignore */ }
}

async function loadArticle() {
  const { data } = await getArticleById(Number(route.params.id))
  form.value = {
    title: data.title,
    slug: data.slug,
    content: data.content,
    summary: data.summary || '',
    cover_image: data.cover_image || '',
    category_id: data.category?.id || undefined,
    tag_ids: data.tags?.map((t: Tag) => t.id) || [],
    status: data.status,
    is_top: data.is_top,
  }
}

function generateSlug() {
  const title = form.value.title
  form.value.slug = title
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .replace(/[-\s]+/g, '-')
    .trim()
}

async function save(status?: string) {
  saveError.value = ''
  saving.value = true
  try {
    const payload = {
      ...form.value,
      status: status || form.value.status,
    }
    if (isEdit.value) {
      await updateArticle(Number(route.params.id), payload)
    } else {
      await createArticle(payload)
    }
    router.push('/admin/articles')
  } catch (e) {
    saveError.value = '保存文章失败'
  } finally {
    saving.value = false
  }
}

function toggleTag(tagId: number) {
  const idx = form.value.tag_ids.indexOf(tagId)
  if (idx >= 0) {
    form.value.tag_ids.splice(idx, 1)
  } else {
    form.value.tag_ids.push(tagId)
  }
}
</script>

<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">{{ isEdit ? '编辑文章' : '新建文章' }}</h1>
      <div class="header-actions">
        <button class="btn" @click="save('draft')" :disabled="saving">保存草稿</button>
        <button class="btn btn-primary" @click="save('published')" :disabled="saving">
          {{ saving ? '保存中...' : '发布' }}
        </button>
      </div>
    </div>

    <div v-if="saveError" class="save-error">{{ saveError }}</div>

    <div v-if="loading" class="loading"><span>加载中...</span></div>
    <template v-else>
      <div class="editor-wrapper">
        <!-- 左侧编辑区 -->
        <div class="editor-main">
          <input
            v-model="form.title"
            class="title-input"
            placeholder="文章标题..."
            @input="generateSlug"
          />
          <div class="slug-row">
            <label>别名：</label>
            <input v-model="form.slug" placeholder="article-slug" />
          </div>
          <!-- Markdown 编辑器 -->
          <MdEditor v-model="form.content" style="height: 500px;" />
        </div>

        <!-- 右侧元数据面板 -->
        <aside class="editor-sidebar card">
          <div class="sidebar-section">
            <h3>状态</h3>
            <select v-model="form.status">
              <option value="draft">草稿</option>
              <option value="published">已发布</option>
            </select>
          </div>
          <div class="sidebar-section">
            <label class="checkbox-label">
              <input type="checkbox" v-model="form.is_top" />
              置顶
            </label>
          </div>
          <div class="sidebar-section">
            <h3>分类</h3>
            <select v-model="form.category_id">
              <option :value="undefined">无分类</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
            </select>
          </div>
          <div class="sidebar-section">
            <h3>标签</h3>
            <div class="tag-selector">
              <label v-for="tag in tags" :key="tag.id" class="tag-option" :class="{ selected: form.tag_ids.includes(tag.id) }">
                <input type="checkbox" :value="tag.id" :checked="form.tag_ids.includes(tag.id)" @change="toggleTag(tag.id)" />
                {{ tag.name }}
              </label>
            </div>
          </div>
          <div class="sidebar-section">
            <h3>封面图片URL</h3>
            <input v-model="form.cover_image" placeholder="https://..." />
          </div>
          <div class="sidebar-section">
            <h3>摘要</h3>
            <textarea v-model="form.summary" placeholder="可选摘要..." rows="3" />
          </div>
        </aside>
      </div>
    </template>
  </div>
</template>

<style scoped lang="scss">
@use '@/assets/styles/variables' as *;

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.page-title { margin-bottom: 0; }

.header-actions {
  display: flex;
  gap: 8px;
}

.save-error {
  background: rgba(245, 108, 108, 0.08);
  color: $danger;
  padding: 10px 14px;
  border-radius: $radius-sm;
  margin-bottom: 16px;
  border-left: 3px solid $danger;
}

.editor-wrapper {
  display: flex;
  gap: 24px;
}

.editor-main {
  flex: 1;
  min-width: 0;
  overflow: hidden;
}

.title-input {
  width: 100%;
  padding: 12px 0;
  border: none;
  border-bottom: 2px solid $border-light;
  font-size: 24px;
  font-weight: 600;
  outline: none;
  margin-bottom: 8px;
  transition: border-color $transition-normal;
  background: transparent;

  &:focus {
    border-bottom-color: $primary;
    border-image: $gradient-primary;
    border-image-slice: 1;
  }
}

.slug-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  font-size: 14px;
  color: $text-secondary;

  input {
    flex: 1;
    padding: 6px 12px;
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

.editor-sidebar {
  width: 300px;
  flex-shrink: 0;
  height: fit-content;
  position: sticky;
  top: 84px;
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
}

.sidebar-section {
  margin-bottom: 20px;

  h3 {
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 8px;
    color: $text;
  }

  select, input[type="text"], input[type="email"], input[type="password"], textarea {
    width: 100%;
    padding: 8px 12px;
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

  textarea {
    min-height: 80px;
    resize: vertical;
  }

  input[type="checkbox"] {
    width: auto;
    margin: 0;
  }
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  cursor: pointer;
}

.tag-selector {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tag-option {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  background: $bg;
  border-radius: $radius-xl;
  font-size: 13px;
  cursor: pointer;
  transition: all $transition-fast;
  border: 1px solid transparent;

  input { width: auto; }

  &.selected {
    background: rgba(64, 158, 255, 0.1);
    color: $primary;
    border-color: rgba(64, 158, 255, 0.3);
  }

  &:hover {
    background: rgba(64, 158, 255, 0.06);
  }
}

@media (max-width: 1024px) {
  .editor-wrapper {
    flex-direction: column;
  }

  .editor-sidebar {
    width: 100%;
    position: static;
  }
}
</style>
