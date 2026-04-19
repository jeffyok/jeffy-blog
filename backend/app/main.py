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

# 注册 C 端 API 路由
from app.api.frontend import all_routers as frontend_routers
for router in frontend_routers:
    app.include_router(router)

# 注册管理端 API 路由
from app.api.admin import all_routers as admin_routers
for router in admin_routers:
    app.include_router(router)


@app.get("/api/health")
async def health_check():
    """健康检查接口"""
    return {"status": "ok"}
