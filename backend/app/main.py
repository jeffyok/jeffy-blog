"""
FastAPI 应用入口
注册所有路由、中间件和生命周期事件
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期：启动时测试数据库连接，关闭时释放引擎"""
    from app.db.session import async_engine
    from sqlalchemy import text
    # 启动时验证数据库连接是否正常
    async with async_engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    yield
    # 关闭时释放数据库引擎资源
    await async_engine.dispose()


app = FastAPI(
    title="Jeffy Blog API",
    description="个人博客后端 API",
    version="1.0.0",
    lifespan=lifespan,
)

# 调试中间件：打印请求信息
@app.middleware("http")
async def debug_middleware(request, call_next):
    if "/api/articles/" in str(request.url):
        print(f"[DEBUG] Request URL: {request.url}")
        print(f"[DEBUG] Query params: {request.query_params}")
    response = await call_next(request)
    return response

# 注册跨域中间件，允许前端跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册所有 API 路由
from app.api.auth import router as auth_router
from app.api.articles import router as articles_router
from app.api.categories import router as categories_router
from app.api.tags import router as tags_router
from app.api.comments import router as comments_router
from app.api.likes import router as likes_router
from app.api.friend_links import router as friend_links_router
from app.api.archives import router as archives_router
from app.api.feed import router as feed_router
from app.api.admin import router as admin_router

app.include_router(auth_router)
app.include_router(articles_router)
app.include_router(categories_router)
app.include_router(tags_router)
app.include_router(comments_router)
app.include_router(likes_router)
app.include_router(friend_links_router)
app.include_router(archives_router)
app.include_router(feed_router)
app.include_router(admin_router)


@app.get("/api/health")
async def health_check():
    """健康检查接口"""
    return {"status": "ok"}
