# Jeffy Blog

个人博客全栈项目，前端 Vue 3，后端 Python FastAPI。

## 技术栈

**前端** — Vue 3.5 + TypeScript + Vite + Pinia + Vue Router + SCSS + Axios + md-editor-v3 + highlight.js

**后端** — Python 3 + FastAPI + SQLAlchemy 2.0 (async) + MySQL (aiomysql) + Alembic + JWT + bcrypt

## 项目结构

```
jeffy-blog/
├── frontend/                  # Vue 3 前端
│   ├── src/
│   │   ├── api/               # Axios 请求模块（按功能拆分）
│   │   ├── assets/styles/     # SCSS 样式（main.scss, variables.scss, markdown.scss）
│   │   ├── components/        # 组件（article/、common/）
│   │   ├── composables/       # 组合式函数
│   │   ├── layouts/           # 布局组件（DefaultLayout, AdminLayout）
│   │   ├── router/            # 路由配置（含导航守卫）
│   │   ├── stores/            # Pinia 状态管理
│   │   ├── types/             # TypeScript 类型定义
│   │   ├── utils/             # 工具函数
│   │   └── views/             # 页面组件（admin/、article/、auth/ 等）
│   ├── vite.config.ts         # Vite 配置（端口 5173，API 代理到 :8000）
│   └── package.json
├── backend/                   # FastAPI 后端
│   ├── app/
│   │   ├── api/               # API 路由（auth, articles, categories, tags, comments, likes, friend_links, archives, feed, admin）
│   │   ├── core/              # 核心配置（config.py, security.py）
│   │   ├── db/                # 数据库会话（SQLAlchemy async engine）
│   │   ├── models/            # ORM 模型（User, Article, Category, Tag, Comment, Like, FriendLink）
│   │   ├── schemas/           # Pydantic 请求/响应模型
│   │   ├── services/          # 业务逻辑层
│   │   └── utils/             # 工具函数（markdown 渲染、slug 生成）
│   ├── alembic/               # 数据库迁移
│   ├── alembic.ini
│   └── requirements.txt
└── .gitignore
```

## 常用命令

### 前端
```bash
cd frontend
npm run dev      # 启动开发服务器（:5173）
npm run build    # 构建生产版本
npm run preview  # 预览生产构建
```

### 后端
```bash
cd backend
uvicorn app.main:app --reload   # 启动开发服务器（:8000）
alembic revision --autogenerate -m "描述"  # 生成迁移
alembic upgrade head            # 执行迁移
alembic downgrade -1            # 回滚一次
```

## 架构约定

- **后端分层**: API 路由 → Service 层 → Model 层，Pydantic Schema 做数据校验
- **后端异步**: 全面使用 async/await，数据库通过 aiomysql 驱动
- **认证**: JWT + OAuth2PasswordBearer，bcrypt 哈希密码，支持 user/admin 角色权限
- **前端状态**: Pinia stores（auth, app, articles），路由守卫控制登录/管理员权限
- **API 代理**: 开发环境 Vite 将 `/api` 请求代理到后端 `:8000`
- **环境变量**: 后端配置在 `backend/.env`（已被 gitignore），通过 pydantic-settings 加载
- **路径别名**: 前端 `@` 映射到 `src/` 目录

## API 路由前缀

| 模块 | 路径 |
|------|------|
| 认证 | `/api/auth` |
| 文章 | `/api/articles` |
| 分类 | `/api/categories` |
| 标签 | `/api/tags` |
| 评论 | `/api/comments` |
| 点赞 | `/api/likes` |
| 友链 | `/api/friend_links` |
| 归档 | `/api/archives` |
| RSS | `/api/feed` |
| 管理 | `/api/admin` |
| 健康检查 | `/api/health` |
