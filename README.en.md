<p align="center">
  <a href="README.md">简体中文</a> |
  <a href="README.zh-TW.md">繁體中文</a> |
  <a href="README.en.md">English</a>
</p>

<div align="center">

# 🎨 MarkCraft Studio

**Lightweight Markdown/HTML Intelligent Editing & Multi-Platform Publishing Engine**

[![PyPI Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/gitstq/MarkCraft-Studio)
[![Python](https://img.shields.io/badge/Python-3.9+-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-35%20passed-success)](tests/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)]()

Convert Markdown to beautifully styled HTML, PDF, DOCX, and PNG with one click. Features 5 built-in themes, live preview, and a zero-dependency core engine.

</div>

---

## 🎉 Introduction

MarkCraft Studio is a **lightweight Markdown/HTML intelligent editing and multi-platform publishing engine built entirely in Python**. Inspired by the explosive growth of AI-era content creation tools (such as html-anything), we aim to provide a **zero-dependency, offline-first, CJK-optimized** localized solution.

### 💡 Problems We Solve

- ❌ Existing tools require Node.js environments or online AI APIs — high deployment barrier
- ❌ Insufficient CJK (Chinese/Japanese/Korean) typography support — missing font fallbacks, punctuation handling, line spacing optimization
- ❌ Multi-format export requires combining multiple tools — fragmented workflows
- ❌ Lack of lightweight local visual editors

### ✨ Key Differentiators

- 🐍 **Pure Python** — Core engine has zero external dependencies, just `pip install` and go
- 🌏 **CJK Typography** — Native CJK-friendly font stacks, proper line spacing, and punctuation handling
- 🎨 **5 Beautiful Themes** — Minimal, Elegant, Tech, Warm, and Dark — covering major aesthetic preferences
- 📤 **4 Export Formats** — One-click conversion to HTML / PDF / DOCX / PNG
- 🖥️ **Dual-Mode** — CLI command-line tool + Web visual editor
- 📝 **Built-in Templates** — Tech article, README, study notes, and presentation templates ready to use
- ⚡ **Offline-First** — No internet connection required, all processing happens locally

---

## ✨ Core Features

| Feature | Description |
|---------|-------------|
| 📝 **Full GFM Support** | Headings, lists, tables, code blocks, task lists, blockquotes, strikethrough, and more |
| 🎨 **5 Theme Presets** | Minimal / Elegant / Tech / Warm / Dark — switch with one click |
| 📤 **Multi-Format Export** | HTML (responsive), PDF (high-quality), DOCX (Word), PNG (image) |
| 🖥️ **Web Editor** | Live preview, theme switching, one-click export, copy HTML fragments |
| 📊 **Smart Stats** | Auto word count, reading time estimation, heading-based TOC generation |
| 📋 **Built-in Templates** | 4 templates: tech article, README, study notes, presentation |
| 🔧 **CLI Tool** | Complete command-line interface for scripted batch processing |
| 🌏 **CJK Optimized** | CJK-friendly font stacks, proper spacing, responsive layout |
| 🧪 **35 Tests** | Comprehensive unit test coverage ensuring code quality |
| 📦 **Zero Core Dependencies** | Core engine relies only on Python standard library |

---

## 🚀 Quick Start

### Requirements

- **Python** 3.9 or higher
- **pip** package manager

### Installation

```bash
# Core installation (zero external dependencies)
pip install markcraft-studio

# Install all features (Web editor, PDF/DOCX/PNG export)
pip install markcraft-studio[all]

# Or install selectively
pip install markcraft-studio[web]     # Web visual editor
pip install markcraft-studio[pdf]     # PDF export
pip install markcraft-studio[docx]    # DOCX export
pip install markcraft-studio[png]     # PNG export
```

### CLI Usage

```bash
# Convert Markdown to HTML
markcraft convert input.md -o output.html

# Convert to PDF (requires pdf extension)
markcraft convert input.md -f pdf -o output.pdf

# Convert to DOCX (requires docx extension)
markcraft convert input.md -f docx -o output.docx

# Export to all formats at once
markcraft convert input.md -f all

# Specify a theme
markcraft convert input.md -t dark -o output.html

# Launch the Web visual editor
markcraft serve

# Quick preview a file
markcraft preview input.md

# List available themes
markcraft themes

# Show version info
markcraft version
```

### Python API

```python
from markcraft.core.engine import MarkCraftEngine, ExportConfig, ThemePreset

# Create engine
engine = MarkCraftEngine()

# Read Markdown file
with open("article.md", "r", encoding="utf-8") as f:
    markdown_text = f.read()

# Convert to full HTML document
html = engine.to_html(markdown_text, config=ExportConfig(
    title="My Article",
    author="Author Name",
    theme=ThemePreset.ELEGANT,
))

# Save HTML file
with open("output.html", "w", encoding="utf-8") as f:
    f.write(html)

# Use export manager (supports multiple formats)
from markcraft.exporters import ExportManager
manager = ExportManager()
manager.export(markdown_text, "output.pdf", ExportConfig(format=OutputFormat.PDF))
```

---

## 📖 Detailed Guide

### Theme Switching

MarkCraft Studio includes 5 carefully designed themes:

| Theme | ID | Style | Best For |
|-------|-----|-------|----------|
| 🌙 Dark | `dark` | Dark background + red accent | Tech docs, code showcases |
| 📄 Minimal | `minimal` | White background + blue accent | General docs, printing |
| ✨ Elegant | `elegant` | Serif fonts + blue accent | Blog posts, formal documents |
| 💻 Tech | `tech` | GitHub-style dark | Developer docs, API docs |
| 🌅 Warm | `warm` | Cream background + gold accent | Long-form reading, notes |

### Custom CSS

```bash
# Use a custom CSS file
markcraft convert input.md -o output.html --css custom.css
```

```python
# Use custom CSS in Python API
config = ExportConfig(css_custom="body { font-size: 18px; }")
html = engine.to_html(markdown_text, config)
```

### Built-in Templates

```python
from markcraft.templates import get_template

# Get tech article template
article_template = get_template('article')

# Get README template
readme_template = get_template('readme')

# Get study notes template
notes_template = get_template('notes')

# Get presentation template
slide_template = get_template('slide')
```

### Web Visual Editor

```bash
# Launch Web editor (default port 8765)
markcraft serve

# Custom port
markcraft serve -p 9000

# Bind to all interfaces
markcraft serve -H 0.0.0.0 -p 9000
```

Web editor features:
- 📝 Left-side Markdown editor with right-side live preview
- 🎨 Real-time theme switching
- 📥 One-click HTML file export
- 📋 Copy HTML fragments to clipboard
- 📊 Real-time word count and reading time estimation

---

## 💡 Design Philosophy & Roadmap

### Design Principles

1. **Offline-First** — All processing happens locally, no internet needed, protecting user privacy
2. **Zero-Dependency Core** — Core engine relies only on Python standard library, minimizing installation friction
3. **Progressive Enhancement** — Core features need zero dependencies; advanced features (PDF/DOCX/Web) install on demand
4. **CJK-Friendly** — Font stacks, spacing, and character counting are optimized for CJK text

### Tech Stack

| Component | Choice | Reason |
|-----------|--------|--------|
| Core Engine | Pure Python | Zero dependencies, cross-platform, easy to maintain |
| Web Framework | Flask | Lightweight, flexible, active community |
| PDF Rendering | WeasyPrint | Pure Python, excellent CSS support |
| DOCX Generation | python-docx | Mature, stable, feature-complete |
| Image Processing | Pillow | Python's standard image processing library |

### Roadmap

- [ ] 🔄 **v1.1** — MathJax/LaTeX math formula support
- [ ] 📊 **v1.2** — Mermaid diagram rendering
- [ ] 🎨 **v1.3** — Custom theme file import
- [ ] 🔌 **v1.4** — Plugin system for extending export formats
- [ ] 🌐 **v1.5** — Multi-language document templates
- [ ] 📱 **v2.0** — Desktop GUI application (based on PyQt/PySide)

---

## 📦 Packaging & Deployment

### Install as a Library

```bash
pip install markcraft-studio
```

### Install from Source

```bash
git clone https://github.com/gitstq/MarkCraft-Studio.git
cd MarkCraft-Studio
pip install -e ".[all]"
```

### Development Setup

```bash
git clone https://github.com/gitstq/MarkCraft-Studio.git
cd MarkCraft-Studio
pip install -e ".[dev,all]"
pytest tests/ -v
```

### Compatible Environments

| Environment | Minimum | Recommended |
|-------------|---------|-------------|
| Python | 3.9 | 3.11+ |
| OS | Windows 10 / macOS 12 / Ubuntu 20.04 | Latest |
| pip | 21.0 | Latest |

---

## 🤝 Contributing

We welcome all forms of contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Commit Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation updates
- `refactor:` Code refactoring
- `test:` Test-related changes
- `chore:` Build/tooling changes

### Issue Reporting

Please submit via [GitHub Issues](https://github.com/gitstq/MarkCraft-Studio/issues) with:

1. Problem description
2. Steps to reproduce
3. Expected behavior
4. Environment info (Python version, OS)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

**Crafted with ❤️ by MarkCraft Studio**

If you find it useful, please give us a ⭐ Star!

</div>
