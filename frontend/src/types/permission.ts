/**
 * 权限和角色类型定义
 */
export interface Permission {
  id: number
  name: string
  display_name: string
  module: string
  created_at: string
}

export interface Role {
  id: number
  name: string
  display_name: string
  description: string | null
  is_default: boolean
  created_at: string
}

export interface RoleWithPermissions extends Role {
  permission_ids: number[]
}
