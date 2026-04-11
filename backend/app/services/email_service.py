"""邮件服务 - 发送通知邮件（新评论、回复通知）"""

import aiosmtplib
from email.message import EmailMessage

from app.core.config import settings


class EmailService:
    """邮件服务类 - 基于SMTP发送异步邮件"""

    @staticmethod
    async def send_email(to: str, subject: str, body: str):
        """发送邮件 - SMTP未配置时静默跳过"""
        if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
            return  # SMTP未配置，跳过发送

        # 构建邮件消息
        msg = EmailMessage()
        msg["From"] = settings.SMTP_USER
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(body, subtype="html")  # HTML格式内容

        # 通过SMTP发送邮件
        await aiosmtplib.send(
            msg,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            start_tls=True,
        )

    @staticmethod
    async def notify_new_comment(article_title: str, comment_content: str, author_email: str):
        """通知文章作者有新评论"""
        html = f"""
        <h2>New Comment on "{article_title}"</h2>
        <p>{comment_content}</p>
        <p><a href="{settings.SITE_URL}">View Blog</a></p>
        """
        await EmailService.send_email(author_email, f"New comment on: {article_title}", html)

    @staticmethod
    async def notify_reply(comment_content: str, reply_content: str, parent_author_email: str):
        """通知评论者有新的回复"""
        html = f"""
        <h2>Someone replied to your comment</h2>
        <p><strong>Your comment:</strong> {comment_content}</p>
        <p><strong>Reply:</strong> {reply_content}</p>
        <p><a href="{settings.SITE_URL}">View Blog</a></p>
        """
        await EmailService.send_email(parent_author_email, "New reply to your comment", html)
