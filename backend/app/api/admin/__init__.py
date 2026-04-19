"""管理后台 API 路由包"""

from app.api.admin.dashboard import router as dashboard_router
from app.api.admin.users import router as users_router
from app.api.admin.articles import router as articles_router
from app.api.admin.categories import router as categories_router
from app.api.admin.tags import router as tags_router
from app.api.admin.comments import router as comments_router
from app.api.admin.friend_links import router as friend_links_router

all_routers = [
    dashboard_router,
    users_router,
    articles_router,
    categories_router,
    tags_router,
    comments_router,
    friend_links_router,
]
