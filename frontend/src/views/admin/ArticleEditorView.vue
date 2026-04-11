<!-- 文章编辑器页面：新建/编辑文章，Markdown 编辑 + 右侧元数据面板 -->
<script setup lang="ts">
import { ref, onMounted, computed, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { MdEditor } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import { getArticle, createArticle, updateArticle } from '@/api/articles'
import { getCategories } from '@/api/categories'
import { getTags } from '@/api/tags'
import type { Article, Category, Tag } from '@/types/article'

const route = useRoute()
const router = useRouter()
// 根据 URL 是否包含 id 判断是新建还是编辑
const isEdit = computed(() => !!route.params.id)
const loading = ref(true)
const saving = ref(false)
const saveError = ref('')

// 文章表单数据
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
  // 并行加载分类、标签，编辑模式下还需加载文章数据
  await Promise.all([loadCategories(), loadTags()])
  if (isEdit.value) {
    await loadArticle()
  }
  loading.value = false
})

onBeforeUnmount(() => {
  // 清理自动保存定时器
  if (autoSaveTimer) clearTimeout(autoSaveTimer)
})

/** 加载分类列表 */
async function loadCategories() {
  try {
    const { data } = await getCategories()
    categories.value = data
  } catch { /* ignore */ }
}

/** 加载标签列表 */
async function loadTags() {
  try {
    const { data } = await getTags()
    tags.value = data
  } catch { /* ignore */ }
}

/** 编辑模式下加载已有文章数据 */
async function loadArticle() {
  const { data } = await getArticle(String(route.params.id))
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

/** 根据标题自动生成 slug */
function generateSlug() {
  const title = form.value.title
  form.value.slug = title
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')     // 移除特殊字符
    .replace(/[-\s]+/g, '-')      // 空格和连字符转为连字符
    .trim()
}

/** 保存文章（可指定状态：draft 或 published） */
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
    router.push('/admin/articles') // 保存成功跳转文章列表
  } catch (e) {
    saveError.value = 'Failed to save article'
  } finally {
    saving.value = false
  }
}

/** 切换标签选中状态 */
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
    <!-- 页头：标题 + 保存/发布按钮 -->
    <div class="page-header">
      <h1 class="page-title">{{ isEdit ? 'Edit Article' : 'New Article' }}</h1>
      <div class="header-actions">
        <button class="btn" @click="save('draft')" :disabled="saving">Save Draft</button>
        <button class="btn btn-primary" @click="save('published')" :disabled="saving">
          {{ saving ? 'Saving...' : 'Publish' }}
        </button>
      </div>
    </div>

    <!-- 保存失败错误提示 -->
    <div v-if="saveError" class="save-error">{{ saveError }}</div>

    <div v-if="loading" class="loading"><span>Loading...</span></div>
    <template v-else>
      <div class="editor-wrapper">
        <!-- 左侧编辑区 -->
        <div class="editor-main">
          <input
            v-model="form.title"
            class="title-input"
            placeholder="Article title..."
            @input="generateSlug"
          />
          <div class="slug-row">
            <label>Slug:</label>
            <input v-model="form.slug" placeholder="article-slug" />
          </div>
          <!-- Markdown 编辑器 -->
          <MdEditor v-model="form.content" language="en-US" style="height: 500px;" />
        </div>

        <!-- 右侧元数据面板 -->
        <aside class="editor-sidebar card">
          <div class="sidebar-section">
            <h3>Status</h3>
            <select v-model="form.status">
              <option value="draft">Draft</option>
              <option value="published">Published</option>
            </select>
          </div>
          <div class="sidebar-section">
            <label>
              <input type="checkbox" v-model="form.is_top" />
              Pin to top
            </label>
          </div>
          <div class="sidebar-section">
            <h3>Category</h3>
            <select v-model="form.category_id">
              <option :value="undefined">No category</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
            </select>
          </div>
          <div class="sidebar-section">
            <h3>Tags</h3>
            <div class="tag-selector">
              <label v-for="tag in tags" :key="tag.id" class="tag-option">
                <input type="checkbox" :value="tag.id" :checked="form.tag_ids.includes(tag.id)" @change="toggleTag(tag.id)" />
                {{ tag.name }}
              </label>
            </div>
          </div>
          <div class="sidebar-section">
            <h3>Cover Image URL</h3>
            <input v-model="form.cover_image" placeholder="https://..." />
          </div>
          <div class="sidebar-section">
            <h3>Summary</h3>
            <textarea v-model="form.summary" placeholder="Optional summary..." rows="3" />
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

.page-title {
  margin-bottom: 0;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.save-error {
  background: #fef0f0;
  color: $danger;
  padding: 8px 12px;
  border-radius: 4px;
  margin-bottom: 16px;
}

.editor-wrapper {
  display: flex;
  gap: 24px;
}

.editor-main {
  flex: 1;
  min-width: 0;
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

  &:focus {
    border-bottom-color: $primary;
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
    border-radius: 4px;
    font-size: 14px;
    outline: none;

    &:focus {
      border-color: $primary;
    }
  }
}

.editor-sidebar {
  width: 300px;
  flex-shrink: 0;
  height: fit-content;
  position: sticky;              // 滚动时固定在顶部
  top: 84px;
}

.sidebar-section {
  margin-bottom: 20px;

  h3 {
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 8px;
    color: $text;
  }

  select, input, textarea {
    width: 100%;
    padding: 8px 12px;
    border: 1px solid $border;
    border-radius: 4px;
    font-size: 14px;
    outline: none;

    &:focus {
      border-color: $primary;
    }
  }

  textarea {
    min-height: 80px;
    resize: vertical;
  }

  label {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 14px;
    cursor: pointer;
  }
}

.tag-selector {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-option {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  background: $bg;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;

  input {
    width: auto;
  }
}

// 中等屏幕以下改为纵向布局
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
