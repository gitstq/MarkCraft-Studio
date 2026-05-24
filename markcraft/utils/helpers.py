"""
MarkCraft Studio 辅助工具函数
"""

import os
import re


def read_file(file_path: str, encoding: str = 'utf-8') -> str:
    """
    读取文件内容

    Args:
        file_path: 文件路径
        encoding: 文件编码

    Returns:
        str: 文件内容
    """
    with open(file_path, 'r', encoding=encoding) as f:
        return f.read()


def write_file(file_path: str, content: str, encoding: str = 'utf-8') -> str:
    """
    写入文件内容

    Args:
        file_path: 文件路径
        content: 写入内容
        encoding: 文件编码

    Returns:
        str: 文件的绝对路径
    """
    directory = os.path.dirname(file_path)
    if directory:
        os.makedirs(directory, exist_ok=True)

    with open(file_path, 'w', encoding=encoding) as f:
        f.write(content)

    return os.path.abspath(file_path)


def count_words(text: str) -> int:
    """
    统计文本字数（支持中英文混合）

    Args:
        text: 文本内容

    Returns:
        int: 字数
    """
    # 中文字符
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    # 英文单词
    english_words = len(re.findall(r'[a-zA-Z]+', text))
    return chinese_chars + english_words


def estimate_reading_time(text: str, words_per_minute: int = 300) -> int:
    """
    估算阅读时间

    Args:
        text: 文本内容
        words_per_minute: 每分钟阅读字数

    Returns:
        int: 预计阅读分钟数
    """
    total_words = count_words(text)
    return max(1, total_words // words_per_minute)


def get_file_extension(file_path: str) -> str:
    """获取文件扩展名"""
    return os.path.splitext(file_path)[1].lower()


def ensure_extension(file_path: str, extension: str) -> str:
    """确保文件具有指定扩展名"""
    if not file_path.endswith(extension):
        file_path += extension
    return file_path
