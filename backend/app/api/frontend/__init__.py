"""C 端 API 路由包"""

from app.api.frontend.auth import router as auth_router
from app.api.frontend.articles import router as articles_router
from app.api.frontend.categories import router as categories_router
from app.api.frontend.tags import router as tags_router
from app.api.frontend.comments import router as comments_router
from app.api.frontend.likes import router as likes_router
from app.api.frontend.friend_links import router as friend_links_router
from app.api.frontend.archives import router as archives_router
from app.api.frontend.feed import router as feed_router

all_routers = [
    auth_router,
    articles_router,
    categories_router,
    tags_router,
    comments_router,
    likes_router,
    friend_links_router,
    archives_router,
    feed_router,
]
