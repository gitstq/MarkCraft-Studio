<p align="center">
  <a href="README.md">简体中文</a> |
  <a href="README.zh-TW.md">繁體中文</a> |
  <a href="README.en.md">English</a>
</p>

<div align="center">

# 🎨 MarkCraft Studio

**AI 驅動的輕量級 Markdown/HTML 智慧編輯與多平台發布引擎**

[![PyPI Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/gitstq/MarkCraft-Studio)
[![Python](https://img.shields.io/badge/Python-3.9+-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-35%20passed-success)](tests/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)]()

一鍵將 Markdown 轉換為精美的 HTML、PDF、DOCX、PNG，支援 5 套主題、即時預覽、零外部依賴核心引擎。

</div>

---

## 🎉 專案介紹

MarkCraft Studio 是一款**純 Python 實現的輕量級 Markdown/HTML 智慧編輯與多平台發布引擎**。靈感來源於當前 AI 時代內容創作工具的爆發式增長（如 html-anything），我們致力於提供一個**零外部核心依賴、離線優先、中文排版最佳化**的本地化解決方案。

### 💡 解決的痛點

- ❌ 現有工具依賴 Node.js 環境或線上 AI API，部署門檻高
- ❌ 中文排版支援不足，字體回退、標點擠壓、行距最佳化缺失
- ❌ 多格式匯出需要多個工具組合，工作流程碎片化
- ❌ 缺少輕量級的本地視覺化編輯器

### ✨ 自研差異化亮點

- 🐍 **純 Python 實現**：核心引擎零外部依賴，`pip install` 即可使用
- 🌏 **中文排版最佳化**：原生中文友善字型棧、合理行距、標點處理
- 🎨 **5 套精美主題**：極簡、優雅、科技、暖色、暗黑，覆蓋主流美學
- 📤 **四格式匯出**：HTML / PDF / DOCX / PNG 一鍵轉換
- 🖥️ **雙模式運行**：CLI 命令列 + Web 視覺化編輯器
- 📝 **內建範本**：技術文章、README、學習筆記、簡報文稿即開即用
- ⚡ **離線優先**：無需網路連接，所有處理在本地完成

---

## ✨ 核心特性

| 特性 | 說明 |
|------|------|
| 📝 **GFM 完整支援** | 標題、列表、表格、程式碼區塊、任務列表、引用、刪除線等 |
| 🎨 **5 套主題預設** | 極簡 / 優雅 / 科技 / 暖色 / 暗黑，一鍵切換 |
| 📤 **多格式匯出** | HTML（響應式）、PDF（高品質）、DOCX（Word）、PNG（圖片） |
| 🖥️ **Web 編輯器** | 即時預覽、主題切換、一鍵匯出、複製 HTML 片段 |
| 📊 **智慧統計** | 自動字數統計、閱讀時間估算、標題目錄生成 |
| 📋 **內建範本** | 技術文章、README、學習筆記、簡報文稿 4 套範本 |
| 🔧 **CLI 工具** | 完整的命令列介面，支援腳本化批次處理 |
| 🌏 **中文最佳化** | 中文友善字型棧、合理排版間距、響應式佈局 |
| 🧪 **35 個測試** | 完整的單元測試覆蓋，程式碼品質有保障 |
| 📦 **零核心依賴** | 核心引擎僅依賴 Python 標準函式庫 |

---

## 🚀 快速開始

### 環境要求

- **Python** 3.9 或更高版本
- **pip** 套件管理器

### 安裝

```bash
# 核心安裝（零外部依賴）
pip install markcraft-studio

# 安裝全部功能（含 Web 編輯器、PDF/DOCX/PNG 匯出）
pip install markcraft-studio[all]

# 或按需安裝
pip install markcraft-studio[web]     # Web 視覺化編輯器
pip install markcraft-studio[pdf]     # PDF 匯出
pip install markcraft-studio[docx]    # DOCX 匯出
pip install markcraft-studio[png]     # PNG 匯出
```

### CLI 使用

```bash
# 轉換 Markdown 為 HTML
markcraft convert input.md -o output.html

# 轉換為 PDF（需安裝 pdf 擴充功能）
markcraft convert input.md -f pdf -o output.pdf

# 轉換為 DOCX（需安裝 docx 擴充功能）
markcraft convert input.md -f docx -o output.docx

# 一鍵匯出所有格式
markcraft convert input.md -f all

# 指定主題
markcraft convert input.md -t dark -o output.html

# 啟動 Web 視覺化編輯器
markcraft serve

# 快速預覽檔案
markcraft preview input.md

# 查看可用主題
markcraft themes

# 查看版本資訊
markcraft version
```

### Python API 使用

```python
from markcraft.core.engine import MarkCraftEngine, ExportConfig, ThemePreset

# 建立引擎
engine = MarkCraftEngine()

# 讀取 Markdown 檔案
with open("article.md", "r", encoding="utf-8") as f:
    markdown_text = f.read()

# 轉換為完整 HTML 文件
html = engine.to_html(markdown_text, config=ExportConfig(
    title="我的文章",
    author="作者名",
    theme=ThemePreset.ELEGANT,
))

# 儲存 HTML 檔案
with open("output.html", "w", encoding="utf-8") as f:
    f.write(html)

# 使用匯出管理器（支援多格式）
from markcraft.exporters import ExportManager
manager = ExportManager()
manager.export(markdown_text, "output.pdf", ExportConfig(format=OutputFormat.PDF))
```

---

## 📖 詳細使用指南

### 主題切換

MarkCraft Studio 內建 5 套精心設計的主題：

| 主題 | 標識 | 風格 | 適用場景 |
|------|------|------|----------|
| 🌙 暗黑 | `dark` | 深色背景 + 紅色強調 | 技術文件、程式碼展示 |
| 📄 極簡 | `minimal` | 純白背景 + 藍色強調 | 通用文件、列印 |
| ✨ 優雅 | `elegant` | 襯線字型 + 藍色強調 | 部落格文章、正式文件 |
| 💻 科技 | `tech` | GitHub 風格深色 | 開發者文件、API 文件 |
| 🌅 暖色 | `warm` | 米色背景 + 金色強調 | 閱讀型長文、筆記 |

### 自訂 CSS

```bash
# 使用自訂 CSS 檔案
markcraft convert input.md -o output.html --css custom.css
```

```python
# Python API 中使用自訂 CSS
config = ExportConfig(css_custom="body { font-size: 18px; }")
html = engine.to_html(markdown_text, config)
```

### 內建範本

```python
from markcraft.templates import get_template

# 取得技術文章範本
article_template = get_template('article')

# 取得 README 範本
readme_template = get_template('readme')

# 取得學習筆記範本
notes_template = get_template('notes')

# 取得簡報文稿範本
slide_template = get_template('slide')
```

### Web 視覺化編輯器

```bash
# 啟動 Web 編輯器（預設連接埠 8765）
markcraft serve

# 自訂連接埠
markcraft serve -p 9000

# 指定綁定位址
markcraft serve -H 0.0.0.0 -p 9000
```

Web 編輯器功能：
- 📝 左側 Markdown 編輯區，右側即時預覽
- 🎨 主題即時切換
- 📥 一鍵匯出 HTML 檔案
- 📋 複製 HTML 片段到剪貼簿
- 📊 即時字數統計和閱讀時間估算

---

## 💡 設計思路與迭代規劃

### 設計理念

1. **離線優先**：所有處理在本地完成，無需網路連接，保護使用者隱私
2. **零依賴核心**：核心引擎僅依賴 Python 標準函式庫，降低安裝門檻
3. **漸進增強**：核心功能零依賴，進階功能（PDF/DOCX/Web）按需安裝
4. **中文友善**：字型棧、排版間距、字元統計均針對中文最佳化

### 技術選型

| 元件 | 技術選擇 | 原因 |
|------|----------|------|
| 核心引擎 | 純 Python | 零依賴、跨平台、易維護 |
| Web 框架 | Flask | 輕量、靈活、社群活躍 |
| PDF 渲染 | WeasyPrint | 純 Python、CSS 支援好 |
| DOCX 生成 | python-docx | 成熟穩定、功能完善 |
| 圖片處理 | Pillow | Python 圖片處理標準函式庫 |

### 後續迭代計畫

- [ ] 🔄 **v1.1**：新增 MathJax/LaTeX 數學公式支援
- [ ] 📊 **v1.2**：新增 Mermaid 圖表渲染
- [ ] 🎨 **v1.3**：支援自訂主題檔案匯入
- [ ] 🔌 **v1.4**：新增外掛系統，支援擴展匯出格式
- [ ] 🌐 **v1.5**：新增多語言文件範本
- [ ] 📱 **v2.0**：新增桌面 GUI 應用（基於 PyQt/PySide）

---

## 📦 打包與部署指南

### 作為函式庫安裝

```bash
pip install markcraft-studio
```

### 從原始碼安裝

```bash
git clone https://github.com/gitstq/MarkCraft-Studio.git
cd MarkCraft-Studio
pip install -e ".[all]"
```

### 開發環境

```bash
git clone https://github.com/gitstq/MarkCraft-Studio.git
cd MarkCraft-Studio
pip install -e ".[dev,all]"
pytest tests/ -v
```

### 相容環境

| 環境 | 最低版本 | 推薦版本 |
|------|----------|----------|
| Python | 3.9 | 3.11+ |
| 作業系統 | Windows 10 / macOS 12 / Ubuntu 20.04 | 最新版 |
| pip | 21.0 | 最新版 |

---

## 🤝 貢獻指南

我們歡迎所有形式的貢獻！請查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解詳情。

### 提交規範

使用 [Conventional Commits](https://www.conventionalcommits.org/) 規範：

- `feat:` 新增功能
- `fix:` 修復問題
- `docs:` 文件更新
- `refactor:` 程式碼重構
- `test:` 測試相關
- `chore:` 建構/工具相關

### Issue 回報

請透過 [GitHub Issues](https://github.com/gitstq/MarkCraft-Studio/issues) 提交，包含：

1. 問題描述
2. 重現步驟
3. 期望行為
4. 環境資訊（Python 版本、作業系統）

---

## 📄 開源協議

本專案基於 [MIT License](LICENSE) 開源。

---

<div align="center">

**由 MarkCraft Studio 用心打造 ⚡**

如果覺得有用，歡迎給個 ⭐ Star 支援一下！

</div>
