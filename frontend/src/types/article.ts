/**
 * 文章相关类型定义
 */

/** 标签 */
export interface Tag {
  id: number
  name: string
  slug: string
  created_at: string
}

/** 分类 */
export interface Category {
  id: number
  name: string
  slug: string
  description: string | null
  created_at: string
}

/** 作者简要信息 */
export interface Author {
  id: number
  username: string
  avatar: string | null
}

/** 文章列表项（不含正文） */
export interface ArticleListItem {
  id: number
  title: string
  slug: string
  summary: string | null
  cover_image: string | null
  category: Category | null
  tags: Tag[]
  author: Author
  status: string
  is_top: boolean
  view_count: number
  like_count: number
  created_at: string
  updated_at: string
}

/** 文章详情（含正文） */
export interface Article extends ArticleListItem {
  content: string
  content_html: string | null
}

/** 文章分页响应 */
export interface ArticlePagination {
  items: ArticleListItem[]
  total: number
  page: number
  page_size: number
}

/** 创建文章请求体 */
export interface ArticleCreate {
  title: string
  slug?: string
  content: string
  summary?: string
  cover_image?: string
  category_id?: number
  tag_ids?: number[]
  status?: string
  is_top?: boolean
}

/** 更新文章请求体（所有字段可选） */
export interface ArticleUpdate extends Partial<ArticleCreate> {}
