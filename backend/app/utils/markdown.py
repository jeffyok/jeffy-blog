"""Markdown工具模块 - 提供Markdown渲染和摘要提取功能"""

import re
import markdown


def render_markdown(md_text: str) -> str:
    """将Markdown文本渲染为HTML - 启用代码高亮、表格、目录等扩展"""
    return markdown.markdown(
        md_text,
        extensions=[
            "fenced_code",   # 围栏代码块
            "tables",        # 表格支持
            "nl2br",         # 换行符转<br>
            "sane_lists",    # 更智能的列表解析
            "toc",           # 目录生成
            "codehilite",    # 代码高亮
        ],
    )


def extract_summary(md_text: str, max_length: int = 200) -> str:
    """从Markdown文本中提取纯文本摘要 - 去除标记语法后截取指定长度"""
    text = md_text.strip()
    # 移除Markdown图片语法
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    # 移除Markdown链接语法
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)
    # 移除标题标记
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
    # 移除行内格式标记（加粗、斜体、代码、删除线）
    text = re.sub(r'[*_`~]', '', text)
    text = text.strip()
    # 超过最大长度时截断并添加省略号
    if len(text) > max_length:
        text = text[:max_length] + "..."
    return text
