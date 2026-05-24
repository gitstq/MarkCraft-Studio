"""
MarkCraft Studio 内置模板
提供常用的Markdown文档模板
"""

TEMPLATES = {
    'article': {
        'name': '技术文章',
        'description': '标准技术博客文章模板',
        'content': """---
title: 文章标题
author: 作者名
date: 2026-01-01
tags: [技术, 教程]
---

# 文章标题

> 一句话摘要，描述文章的核心内容。

## 📋 前言

简要介绍文章的背景和目的。

## ✨ 核心内容

### 要点一

详细描述第一个要点...

### 要点二

详细描述第二个要点...

**重点内容**使用粗体标注。

### 代码示例

```python
def hello():
    print("Hello, MarkCraft Studio!")
```

## 📊 数据对比

| 特性 | 方案A | 方案B |
|------|-------|-------|
| 性能 | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| 易用性 | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| 扩展性 | ⭐⭐ | ⭐⭐⭐⭐ |

## 🎯 总结

- 要点回顾一
- 要点回顾二
- 要点回顾三

---

*本文由 MarkCraft Studio 生成*
""",
    },
    'readme': {
        'name': 'README文档',
        'description': 'GitHub项目README模板',
        'content': """# 项目名称

> 一句话描述项目功能

![License](https://img.shields.io/badge/license-MIT-blue)
![Version](https://img.shields.io/badge/version-1.0.0-green)

## ✨ 特性

- 特性一：描述
- 特性二：描述
- 特性三：描述

## 🚀 快速开始

### 环境要求

- Python 3.9+
- pip

### 安装

```bash
pip install project-name
```

### 使用

```python
from project import main

main()
```

## 📖 文档

详细文档请参考 [文档链接](#)

## 🤝 贡献

欢迎提交 Issue 和 PR！

## 📄 开源协议

MIT License
""",
    },
    'notes': {
        'name': '学习笔记',
        'description': '学习笔记模板',
        'content': """# 学习笔记标题

**日期**：2026-01-01
**主题**：学习主题

## 📝 核心概念

### 概念一

定义和解释...

### 概念二

定义和解释...

## 💡 关键理解

1. 理解要点一
2. 理解要点二
3. 理解要点三

## 🔧 实践练习

### 练习一

问题描述...

**解决方案**：

```
步骤一
步骤二
步骤三
```

## ❓ 疑问与思考

- [ ] 待解决问题一
- [ ] 待解决问题二
- [x] 已解决问题三

## 📚 参考资源

- [资源一](https://example.com)
- [资源二](https://example.com)
""",
    },
    'slide': {
        'name': '演示文稿',
        'description': '幻灯片/演示内容模板',
        'content': """# 演示文稿标题

副标题或作者信息

---

## 第一部分：背景介绍

### 背景

- 背景要点一
- 背景要点二
- 背景要点三

### 问题

> 当前面临的核心挑战是什么？

---

## 第二部分：解决方案

### 方案概述

**核心思路**：简要描述解决方案

### 技术架构

```
输入 → 处理 → 输出
```

### 关键数据

| 指标 | 优化前 | 优化后 | 提升 |
|------|--------|--------|------|
| 性能 | 100ms | 20ms | 5x |
| 内存 | 500MB | 200MB | 60% |

---

## 第三部分：总结

### 核心成果

1. 成果一
2. 成果二
3. 成果三

### 下一步计划

- [ ] 计划一
- [ ] 计划二

---

## 谢谢！

联系方式：email@example.com
""",
    },
}


def get_template(template_name: str) -> str:
    """
    获取指定模板内容

    Args:
        template_name: 模板名称

    Returns:
        str: 模板Markdown内容

    Raises:
        KeyError: 模板不存在
    """
    if template_name not in TEMPLATES:
        available = ', '.join(TEMPLATES.keys())
        raise KeyError(f"模板 '{template_name}' 不存在。可用模板: {available}")

    return TEMPLATES[template_name]['content']


def list_templates() -> dict:
    """
    列出所有可用模板

    Returns:
        dict: 模板信息字典
    """
    return {
        name: {
            'name': info['name'],
            'description': info['description'],
        }
        for name, info in TEMPLATES.items()
    }
