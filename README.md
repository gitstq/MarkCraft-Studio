<p align="center">
  <a href="README.md">简体中文</a> |
  <a href="README.zh-TW.md">繁體中文</a> |
  <a href="README.en.md">English</a>
</p>

<div align="center">

# 🎨 MarkCraft Studio

**AI驱动的轻量级Markdown/HTML智能编辑与多平台发布引擎**

[![PyPI Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/gitstq/MarkCraft-Studio)
[![Python](https://img.shields.io/badge/Python-3.9+-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-35%20passed-success)](tests/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)]()

一键将 Markdown 转换为精美的 HTML、PDF、DOCX、PNG，支持 5 套主题、实时预览、零外部依赖核心引擎。

</div>

---

## 🎉 项目介绍

MarkCraft Studio 是一款**纯 Python 实现的轻量级 Markdown/HTML 智能编辑与多平台发布引擎**。灵感来源于当前 AI 时代内容创作工具的爆发式增长（如 html-anything），我们致力于提供一个**零外部核心依赖、离线优先、中文排版优化**的本地化解决方案。

### 💡 解决的痛点

- ❌ 现有工具依赖 Node.js/Node 环境或在线 AI API，部署门槛高
- ❌ 中文排版支持不足，字体回退、标点挤压、行距优化缺失
- ❌ 多格式导出需要多个工具组合，工作流碎片化
- ❌ 缺少轻量级的本地可视化编辑器

### ✨ 自研差异化亮点

- 🐍 **纯 Python 实现**：核心引擎零外部依赖，`pip install` 即可使用
- 🌏 **中文排版优化**：原生中文友好字体栈、合理行距、标点处理
- 🎨 **5 套精美主题**：极简、优雅、科技、暖色、暗黑，覆盖主流审美
- 📤 **四格式导出**：HTML / PDF / DOCX / PNG 一键转换
- 🖥️ **双模式运行**：CLI 命令行 + Web 可视化编辑器
- 📝 **内置模板**：技术文章、README、学习笔记、演示文稿即开即用
- ⚡ **离线优先**：无需网络连接，所有处理在本地完成

---

## ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 📝 **GFM 完整支持** | 标题、列表、表格、代码块、任务列表、引用、删除线等 |
| 🎨 **5 套主题预设** | 极简 / 优雅 / 科技 / 暖色 / 暗黑，一键切换 |
| 📤 **多格式导出** | HTML（响应式）、PDF（高质量）、DOCX（Word）、PNG（图片） |
| 🖥️ **Web 编辑器** | 实时预览、主题切换、一键导出、复制 HTML 片段 |
| 📊 **智能统计** | 自动字数统计、阅读时间估算、标题目录生成 |
| 📋 **内置模板** | 技术文章、README、学习笔记、演示文稿 4 套模板 |
| 🔧 **CLI 工具** | 完整的命令行接口，支持脚本化批量处理 |
| 🌏 **中文优化** | 中文友好字体栈、合理排版间距、响应式布局 |
| 🧪 **35 个测试** | 完整的单元测试覆盖，代码质量有保障 |
| 📦 **零核心依赖** | 核心引擎仅依赖 Python 标准库 |

---

## 🚀 快速开始

### 环境要求

- **Python** 3.9 或更高版本
- **pip** 包管理器

### 安装

```bash
# 核心安装（零外部依赖）
pip install markcraft-studio

# 安装全部功能（含 Web 编辑器、PDF/DOCX/PNG 导出）
pip install markcraft-studio[all]

# 或按需安装
pip install markcraft-studio[web]     # Web 可视化编辑器
pip install markcraft-studio[pdf]     # PDF 导出
pip install markcraft-studio[docx]    # DOCX 导出
pip install markcraft-studio[png]     # PNG 导出
```

### CLI 使用

```bash
# 转换 Markdown 为 HTML
markcraft convert input.md -o output.html

# 转换为 PDF（需安装 pdf 扩展）
markcraft convert input.md -f pdf -o output.pdf

# 转换为 DOCX（需安装 docx 扩展）
markcraft convert input.md -f docx -o output.docx

# 一键导出所有格式
markcraft convert input.md -f all

# 指定主题
markcraft convert input.md -t dark -o output.html

# 启动 Web 可视化编辑器
markcraft serve

# 快速预览文件
markcraft preview input.md

# 查看可用主题
markcraft themes

# 查看版本信息
markcraft version
```

### Python API 使用

```python
from markcraft.core.engine import MarkCraftEngine, ExportConfig, ThemePreset

# 创建引擎
engine = MarkCraftEngine()

# 读取 Markdown 文件
with open("article.md", "r", encoding="utf-8") as f:
    markdown_text = f.read()

# 转换为完整 HTML 文档
html = engine.to_html(markdown_text, config=ExportConfig(
    title="我的文章",
    author="作者名",
    theme=ThemePreset.ELEGANT,
))

# 保存 HTML 文件
with open("output.html", "w", encoding="utf-8") as f:
    f.write(html)

# 使用导出管理器（支持多格式）
from markcraft.exporters import ExportManager
manager = ExportManager()
manager.export(markdown_text, "output.pdf", ExportConfig(format=OutputFormat.PDF))
```

---

## 📖 详细使用指南

### 主题切换

MarkCraft Studio 内置 5 套精心设计的主题：

| 主题 | 标识 | 风格 | 适用场景 |
|------|------|------|----------|
| 🌙 暗黑 | `dark` | 深色背景 + 红色强调 | 技术文档、代码展示 |
| 📄 极简 | `minimal` | 纯白背景 + 蓝色强调 | 通用文档、打印 |
| ✨ 优雅 | `elegant` | 衬线字体 + 蓝色强调 | 博客文章、正式文档 |
| 💻 科技 | `tech` | GitHub 风格深色 | 开发者文档、API 文档 |
| 🌅 暖色 | `warm` | 米色背景 + 金色强调 | 阅读型长文、笔记 |

### 自定义 CSS

```bash
# 使用自定义 CSS 文件
markcraft convert input.md -o output.html --css custom.css
```

```python
# Python API 中使用自定义 CSS
config = ExportConfig(css_custom="body { font-size: 18px; }")
html = engine.to_html(markdown_text, config)
```

### 内置模板

```bash
# 通过 Python API 使用模板
from markcraft.templates import get_template

# 获取技术文章模板
article_template = get_template('article')

# 获取 README 模板
readme_template = get_template('readme')

# 获取学习笔记模板
notes_template = get_template('notes')

# 获取演示文稿模板
slide_template = get_template('slide')
```

### Web 可视化编辑器

```bash
# 启动 Web 编辑器（默认端口 8765）
markcraft serve

# 自定义端口
markcraft serve -p 9000

# 指定绑定地址
markcraft serve -H 0.0.0.0 -p 9000
```

Web 编辑器功能：
- 📝 左侧 Markdown 编辑区，右侧实时预览
- 🎨 主题实时切换
- 📥 一键导出 HTML 文件
- 📋 复制 HTML 片段到剪贴板
- 📊 实时字数统计和阅读时间估算

---

## 💡 设计思路与迭代规划

### 设计理念

1. **离线优先**：所有处理在本地完成，无需网络连接，保护用户隐私
2. **零依赖核心**：核心引擎仅依赖 Python 标准库，降低安装门槛
3. **渐进增强**：核心功能零依赖，高级功能（PDF/DOCX/Web）按需安装
4. **中文友好**：字体栈、排版间距、字符统计均针对中文优化

### 技术选型

| 组件 | 技术选择 | 原因 |
|------|----------|------|
| 核心引擎 | 纯 Python | 零依赖、跨平台、易维护 |
| Web 框架 | Flask | 轻量、灵活、社区活跃 |
| PDF 渲染 | WeasyPrint | 纯 Python、CSS 支持好 |
| DOCX 生成 | python-docx | 成熟稳定、功能完善 |
| 图片处理 | Pillow | Python 图像处理标准库 |

### 后续迭代计划

- [ ] 🔄 **v1.1**：添加 MathJax/LaTeX 数学公式支持
- [ ] 📊 **v1.2**：添加 Mermaid 图表渲染
- [ ] 🎨 **v1.3**：支持自定义主题文件导入
- [ ] 🔌 **v1.4**：添加插件系统，支持扩展导出格式
- [ ] 🌐 **v1.5**：添加多语言文档模板
- [ ] 📱 **v2.0**：添加桌面 GUI 应用（基于 PyQt/PySide）

---

## 📦 打包与部署指南

### 作为库安装

```bash
pip install markcraft-studio
```

### 从源码安装

```bash
git clone https://github.com/gitstq/MarkCraft-Studio.git
cd MarkCraft-Studio
pip install -e ".[all]"
```

### 开发环境

```bash
git clone https://github.com/gitstq/MarkCraft-Studio.git
cd MarkCraft-Studio
pip install -e ".[dev,all]"
pytest tests/ -v
```

### 兼容环境

| 环境 | 最低版本 | 推荐版本 |
|------|----------|----------|
| Python | 3.9 | 3.11+ |
| 操作系统 | Windows 10 / macOS 12 / Ubuntu 20.04 | 最新版 |
| pip | 21.0 | 最新版 |

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

### 提交规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat:` 新增功能
- `fix:` 修复问题
- `docs:` 文档更新
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建/工具相关

### Issue 反馈

请通过 [GitHub Issues](https://github.com/gitstq/MarkCraft-Studio/issues) 提交，包含：

1. 问题描述
2. 复现步骤
3. 期望行为
4. 环境信息（Python 版本、操作系统）

---

## 📄 开源协议

本项目基于 [MIT License](LICENSE) 开源。

```
MIT License

Copyright (c) 2026 MarkCraft Studio Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

<div align="center">

**由 MarkCraft Studio 用心打造 ⚡**

如果觉得有用，欢迎给个 ⭐ Star 支持一下！

</div>
