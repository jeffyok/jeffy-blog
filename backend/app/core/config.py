"""
应用配置模块
使用 pydantic-settings 从 .env 文件加载配置，支持环境变量覆盖
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """全局配置类，字段会自动从环境变量或 .env 文件读取"""

    model_config = SettingsConfigDict(
        env_file=".env",           # 配置文件路径
        env_file_encoding="utf-8",
        extra="ignore",            # 忽略多余的环境变量
    )

    # 数据库连接地址（异步驱动 aiomysql）
    DATABASE_URL: str = "mysql+aiomysql://root:password@localhost:3306/jeffy_blog"
    # JWT 密钥（生产环境必须修改）
    SECRET_KEY: str = "change-me-to-a-random-secret-key"
    # JWT 加密算法
    ALGORITHM: str = "HS256"
    # 访问令牌过期时间（分钟），默认 24 小时
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    # 站点地址，用于生成 RSS 等绝对链接
    SITE_URL: str = "http://localhost:5173"
    # 允许的跨域来源
    CORS_ORIGINS: list[str] = ["http://localhost:5173"]

    # SMTP 邮件配置（用于评论通知）
    SMTP_HOST: str = "smtp.example.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""


# 全局配置单例
settings = Settings()
