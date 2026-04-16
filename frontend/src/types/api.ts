/**
 * 通用 API 类型定义
 * 包含友情链接、仪表盘统计、归档、分类/标签的增删改类型
 */

/** 友情链接 */
export interface FriendLink {
  id: number
  title: string
  url: string
  logo: string | null
  description: string | null
  sort_order: number
}

/** 创建友情链接 */
export interface FriendLinkCreate {
  title: string
  url: string
  logo?: string
  description?: string
  sort_order?: number
}

/** 更新友情链接 */
export interface FriendLinkUpdate extends Partial<FriendLinkCreate> {}

/** 仪表盘统计数据 */
export interface DashboardStats {
  total_articles: number
  published_articles: number
  draft_articles: number
  total_comments: number
  pending_comments: number
  total_views: number
  total_likes: number
  total_users: number
}

/** 归档中的文章条目 */
export interface ArchiveArticle {
  id: number
  title: string
  slug: string
  created_at: string
  author?: {
    id: number
    username: string
  }
}

/** 归档月份 */
export interface ArchiveMonth {
  month: number
  articles: ArchiveArticle[]
}

/** 归档年份 */
export interface ArchiveYear {
  year: number
  months: ArchiveMonth[]
}

/** 创建分类 */
export interface CategoryCreate {
  name: string
  slug?: string
  description?: string
}

/** 更新分类 */
export interface CategoryUpdate extends Partial<CategoryCreate> {}

/** 创建标签 */
export interface TagCreate {
  name: string
  slug?: string
}

/** 更新标签 */
export interface TagUpdate extends Partial<TagCreate> {}
