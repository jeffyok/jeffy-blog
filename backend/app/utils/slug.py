"""Slug生成工具 - 从标题生成URL友好的标识字符串"""

import re
import uuid


def generate_slug(title: str) -> str:
    """从标题生成URL友好的slug - 转小写、去除特殊字符、空格转连字符，空标题时生成随机字符串"""
    # 移除非字母数字字符，转小写
    slug = re.sub(r'[^\w\s-]', '', title.lower()).strip()
    # 将空格和连续分隔符合并为单个连字符
    slug = re.sub(r'[-\s]+', '-', slug)
    # 空标题时生成8位随机hex字符串
    return slug or uuid.uuid4().hex[:8]
