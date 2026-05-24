"""
MarkCraft Studio 核心引擎
负责Markdown解析、HTML转换、智能排版等核心功能
"""

import re
import os
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass, field
from enum import Enum


class OutputFormat(Enum):
    """支持的输出格式枚举"""
    HTML = "html"
    PDF = "pdf"
    DOCX = "docx"
    PNG = "png"
    MARKDOWN = "markdown"


class ThemePreset(Enum):
    """主题预设枚举"""
    MINIMAL = "minimal"
    ELEGANT = "elegant"
    TECH = "tech"
    WARM = "warm"
    DARK = "dark"


@dataclass
class ExportConfig:
    """导出配置"""
    format: OutputFormat = OutputFormat.HTML
    theme: ThemePreset = ThemePreset.ELEGANT
    title: str = "Untitled Document"
    author: str = ""
    language: str = "zh-CN"
    css_custom: str = ""
    include_toc: bool = True
    highlight_code: bool = True
    responsive: bool = True
    page_size: str = "A4"
    margin: str = "20mm"
    dpi: int = 150
    width: int = 1200
    metadata: Dict = field(default_factory=dict)


@dataclass
class ParseResult:
    """解析结果"""
    html: str
    metadata: Dict
    toc: List[Dict]
    word_count: int
    reading_time: int
    headings: List[Dict]


class MarkdownParser:
    """
    Markdown解析器
    支持GitHub Flavored Markdown (GFM)扩展语法
    """

    # 标题正则
    HEADING_PATTERN = re.compile(r'^(#{1,6})\s+(.+?)(?:\s+\{#(.+?)\})?\s*$', re.MULTILINE)
    # 代码块正则
    CODE_BLOCK_PATTERN = re.compile(r'```(\w*)\n(.*?)```', re.DOTALL)
    # 行内代码正则
    INLINE_CODE_PATTERN = re.compile(r'`([^`]+)`')
    # 图片正则
    IMAGE_PATTERN = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
    # 链接正则
    LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    # 粗体正则
    BOLD_PATTERN = re.compile(r'\*\*(.+?)\*\*|__(.+?)__')
    # 斜体正则
    ITALIC_PATTERN = re.compile(r'\*(.+?)\*|_(.+?)_')
    # 删除线正则
    STRIKETHROUGH_PATTERN = re.compile(r'~~(.+?)~~')
    # 表格正则
    TABLE_PATTERN = re.compile(r'(\|.+\|\n\|[-:\s|]+\|\n(?:\|.+\|\n?)*)')
    # 引用块正则
    BLOCKQUOTE_PATTERN = re.compile(r'^>\s?(.+)$', re.MULTILINE)
    # 无序列表正则
    UNORDERED_LIST_PATTERN = re.compile(r'^(\s*)[-*+]\s+(.+)$', re.MULTILINE)
    # 有序列表正则
    ORDERED_LIST_PATTERN = re.compile(r'^(\s*)\d+\.\s+(.+)$', re.MULTILINE)
    # 水平线正则
    HR_PATTERN = re.compile(r'^(?:---|\*\*\*|___)\s*$', re.MULTILINE)
    # 任务列表正则
    TASK_LIST_PATTERN = re.compile(r'^(\s*)[-*+]\s+\[([ xX])\]\s+(.+)$', re.MULTILINE)

    def __init__(self):
        self._headings: List[Dict] = []
        self._metadata: Dict = {}

    def parse(self, markdown_text: str) -> ParseResult:
        """
        解析Markdown文本为HTML

        Args:
            markdown_text: Markdown原始文本

        Returns:
            ParseResult: 解析结果对象
        """
        self._headings = []
        self._metadata = self._extract_metadata(markdown_text)

        # 移除YAML前置数据
        content = self._strip_frontmatter(markdown_text)

        # 按优先级顺序处理各种元素
        html = content
        html = self._process_code_blocks(html)
        html = self._process_tables(html)
        html = self._process_headings(html)
        html = self._process_blockquotes(html)
        html = self._process_task_lists(html)
        html = self._process_unordered_lists(html)
        html = self._process_ordered_lists(html)
        html = self._process_horizontal_rules(html)
        html = self._process_images(html)
        html = self._process_links(html)
        html = self._process_bold(html)
        html = self._process_italic(html)
        html = self._process_strikethrough(html)
        html = self._process_inline_code(html)
        html = self._process_paragraphs(html)

        # 清理多余空行
        html = re.sub(r'\n{3,}', '\n\n', html)

        # 计算统计信息
        word_count = len(re.findall(r'[\u4e00-\u9fff]|[a-zA-Z]+', content))
        reading_time = max(1, word_count // 300)

        return ParseResult(
            html=html.strip(),
            metadata=self._metadata,
            toc=self._headings,
            word_count=word_count,
            reading_time=reading_time,
            headings=self._headings
        )

    def _extract_metadata(self, text: str) -> Dict:
        """提取YAML前置元数据"""
        metadata = {}
        if text.startswith('---'):
            end = text.find('---', 3)
            if end != -1:
                yaml_block = text[3:end].strip()
                for line in yaml_block.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        metadata[key.strip()] = value.strip().strip('"\'')
        return metadata

    def _strip_frontmatter(self, text: str) -> str:
        """移除YAML前置数据"""
        if text.startswith('---'):
            end = text.find('---', 3)
            if end != -1:
                return text[end + 3:].strip()
        return text

    def _process_code_blocks(self, text: str) -> str:
        """处理代码块"""
        def replace_code_block(match):
            lang = match.group(1) or 'text'
            code = match.group(2).rstrip()
            escaped = code.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            return f'<pre><code class="language-{lang}">{escaped}</code></pre>'

        return self.CODE_BLOCK_PATTERN.sub(replace_code_block, text)

    def _process_inline_code(self, text: str) -> str:
        """处理行内代码"""
        return self.INLINE_CODE_PATTERN.sub(
            r'<code class="inline-code">\1</code>', text
        )

    def _process_headings(self, text: str) -> str:
        """处理标题"""
        def replace_heading(match):
            level = len(match.group(1))
            content = match.group(2)
            anchor = match.group(3) or self._generate_anchor(content)
            self._headings.append({
                'level': level,
                'text': content,
                'anchor': anchor
            })
            return f'<h{level} id="{anchor}">{content}</h{level}>'

        return self.HEADING_PATTERN.sub(replace_heading, text)

    def _process_images(self, text: str) -> str:
        """处理图片"""
        return self.IMAGE_PATTERN.sub(
            r'<figure><img src="\2" alt="\1" loading="lazy"><figcaption>\1</figcaption></figure>',
            text
        )

    def _process_links(self, text: str) -> str:
        """处理链接"""
        return self.LINK_PATTERN.sub(r'<a href="\2" target="_blank" rel="noopener">\1</a>', text)

    def _process_bold(self, text: str) -> str:
        """处理粗体"""
        return self.BOLD_PATTERN.sub(r'<strong>\1\2</strong>', text)

    def _process_italic(self, text: str) -> str:
        """处理斜体"""
        return self.ITALIC_PATTERN.sub(r'<em>\1\2</em>', text)

    def _process_strikethrough(self, text: str) -> str:
        """处理删除线"""
        return self.STRIKETHROUGH_PATTERN.sub(r'<del>\1</del>', text)

    def _process_blockquotes(self, text: str) -> str:
        """处理引用块"""
        def replace_blockquote(match):
            content = match.group(1)
            return f'<blockquote><p>{content}</p></blockquote>'

        return self.BLOCKQUOTE_PATTERN.sub(replace_blockquote, text)

    def _process_tables(self, text: str) -> str:
        """处理表格"""
        def replace_table(match):
            rows = match.group(1).strip().split('\n')
            if len(rows) < 2:
                return match.group(0)

            # 解析表头
            headers = [cell.strip() for cell in rows[0].split('|')[1:-1]]
            # 跳过分隔行
            data_rows = rows[2:] if len(rows) > 2 else []

            html = '<div class="table-wrapper"><table><thead><tr>'
            for h in headers:
                html += f'<th>{h}</th>'
            html += '</tr></thead><tbody>'

            for row in data_rows:
                cells = [cell.strip() for cell in row.split('|')[1:-1]]
                html += '<tr>'
                for cell in cells:
                    html += f'<td>{cell}</td>'
                html += '</tr>'

            html += '</tbody></table></div>'
            return html

        return self.TABLE_PATTERN.sub(replace_table, text)

    def _process_unordered_lists(self, text: str) -> str:
        """处理无序列表"""
        lines = text.split('\n')
        result = []
        in_list = False
        current_indent = 0

        for line in lines:
            ul_match = self.UNORDERED_LIST_PATTERN.match(line)
            if ul_match:
                indent = len(ul_match.group(1))
                content = ul_match.group(2)

                if not in_list:
                    result.append('<ul>')
                    in_list = True
                    current_indent = indent
                elif indent > current_indent:
                    result.append('<ul>')
                    current_indent = indent
                elif indent < current_indent:
                    result.append('</ul>')
                    current_indent = indent

                result.append(f'<li>{content}</li>')
            else:
                if in_list:
                    result.append('</ul>')
                    in_list = False
                result.append(line)

        if in_list:
            result.append('</ul>')

        return '\n'.join(result)

    def _process_ordered_lists(self, text: str) -> str:
        """处理有序列表"""
        lines = text.split('\n')
        result = []
        in_list = False

        for line in lines:
            ol_match = self.ORDERED_LIST_PATTERN.match(line)
            if ol_match:
                content = ol_match.group(2)
                if not in_list:
                    result.append('<ol>')
                    in_list = True
                result.append(f'<li>{content}</li>')
            else:
                if in_list:
                    result.append('</ol>')
                    in_list = False
                result.append(line)

        if in_list:
            result.append('</ol>')

        return '\n'.join(result)

    def _process_task_lists(self, text: str) -> str:
        """处理任务列表"""
        def replace_task(match):
            indent = match.group(1)
            checked = match.group(2).lower() == 'x'
            content = match.group(3)
            checkbox = 'checked' if checked else ''
            return f'{indent}<li class="task-item"><input type="checkbox" {checkbox} disabled>{content}</li>'

        result = self.TASK_LIST_PATTERN.sub(replace_task, text)

        # 包裹任务列表
        result = re.sub(
            r'((?:<li class="task-item">.*?</li>\n?)+)',
            r'<ul class="task-list">\1</ul>',
            result
        )

        return result

    def _process_horizontal_rules(self, text: str) -> str:
        """处理水平线"""
        return self.HR_PATTERN.sub('<hr>', text)

    def _process_paragraphs(self, text: str) -> str:
        """处理段落"""
        lines = text.split('\n')
        result = []
        in_paragraph = False
        in_block = False

        block_tags = {'<h', '<pre', '<ul', '<ol', '<blockquote', '<hr', '<table', '<div', '<figure'}

        for line in lines:
            stripped = line.strip()

            if not stripped:
                if in_paragraph:
                    result.append('</p>')
                    in_paragraph = False
                continue

            # 检查是否是块级元素
            is_block = any(stripped.startswith(tag) for tag in block_tags) or stripped.startswith('</')

            if is_block:
                if in_paragraph:
                    result.append('</p>')
                    in_paragraph = False
                result.append(stripped)
            elif not in_paragraph:
                result.append(f'<p>{stripped}')
                in_paragraph = True
            else:
                result.append(f'<br>{stripped}')

        if in_paragraph:
            result.append('</p>')

        return '\n'.join(result)

    @staticmethod
    def _generate_anchor(text: str) -> str:
        """生成标题锚点"""
        anchor = text.lower().strip()
        anchor = re.sub(r'[^\w\s\u4e00-\u9fff-]', '', anchor)
        anchor = re.sub(r'[\s]+', '-', anchor)
        return anchor


class ThemeEngine:
    """
    主题引擎
    负责生成不同风格的CSS样式
    """

    THEMES = {
        ThemePreset.MINIMAL: {
            'name': '极简',
            'bg': '#ffffff',
            'fg': '#333333',
            'accent': '#0066cc',
            'code_bg': '#f5f5f5',
            'border': '#e0e0e0',
            'font_body': '-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC", sans-serif',
            'font_heading': '-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC", sans-serif',
            'font_code': '"SF Mono", "Fira Code", "Noto Sans Mono", monospace',
        },
        ThemePreset.ELEGANT: {
            'name': '优雅',
            'bg': '#fefefe',
            'fg': '#2c3e50',
            'accent': '#3498db',
            'code_bg': '#f8f9fa',
            'border': '#dee2e6',
            'font_body': 'Georgia, "Noto Serif SC", "Source Han Serif SC", serif',
            'font_heading': '"Helvetica Neue", "Noto Sans SC", sans-serif',
            'font_code': '"SF Mono", "Fira Code", "Noto Sans Mono", monospace',
        },
        ThemePreset.TECH: {
            'name': '科技',
            'bg': '#0d1117',
            'fg': '#c9d1d9',
            'accent': '#58a6ff',
            'code_bg': '#161b22',
            'border': '#30363d',
            'font_body': '-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC", sans-serif',
            'font_heading': '-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC", sans-serif',
            'font_code': '"SF Mono", "Fira Code", "Noto Sans Mono", monospace',
        },
        ThemePreset.WARM: {
            'name': '暖色',
            'bg': '#fdf6e3',
            'fg': '#657b83',
            'accent': '#b58900',
            'code_bg': '#eee8d5',
            'border': '#ddd6c1',
            'font_body': '"Noto Serif SC", Georgia, serif',
            'font_heading': '"Noto Sans SC", "Helvetica Neue", sans-serif',
            'font_code': '"SF Mono", "Fira Code", "Noto Sans Mono", monospace',
        },
        ThemePreset.DARK: {
            'name': '暗黑',
            'bg': '#1a1a2e',
            'fg': '#e0e0e0',
            'accent': '#e94560',
            'code_bg': '#16213e',
            'border': '#0f3460',
            'font_body': '-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC", sans-serif',
            'font_heading': '-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC", sans-serif',
            'font_code': '"SF Mono", "Fira Code", "Noto Sans Mono", monospace',
        },
    }

    @classmethod
    def get_css(cls, theme: ThemePreset, custom_css: str = "", responsive: bool = True) -> str:
        """
        生成主题CSS

        Args:
            theme: 主题预设
            custom_css: 自定义CSS覆盖
            responsive: 是否启用响应式布局

        Returns:
            str: 完整CSS样式字符串
        """
        t = cls.THEMES[theme]

        css = f"""
/* MarkCraft Studio - {t['name']} Theme */
:root {{
    --mc-bg: {t['bg']};
    --mc-fg: {t['fg']};
    --mc-accent: {t['accent']};
    --mc-code-bg: {t['code_bg']};
    --mc-border: {t['border']};
    --mc-font-body: {t['font_body']};
    --mc-font-heading: {t['font_heading']};
    --mc-font-code: {t['font_code']};
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: var(--mc-font-body);
    font-size: 16px;
    line-height: 1.8;
    color: var(--mc-fg);
    background-color: var(--mc-bg);
    padding: 2rem;
    max-width: 800px;
    margin: 0 auto;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}}

h1, h2, h3, h4, h5, h6 {{
    font-family: var(--mc-font-heading);
    font-weight: 700;
    line-height: 1.3;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    color: var(--mc-fg);
}}

h1 {{ font-size: 2em; border-bottom: 2px solid var(--mc-border); padding-bottom: 0.3em; }}
h2 {{ font-size: 1.5em; border-bottom: 1px solid var(--mc-border); padding-bottom: 0.2em; }}
h3 {{ font-size: 1.25em; }}
h4 {{ font-size: 1.1em; }}

p {{
    margin-bottom: 1em;
    text-align: justify;
}}

a {{
    color: var(--mc-accent);
    text-decoration: none;
    border-bottom: 1px solid transparent;
    transition: border-color 0.2s ease;
}}

a:hover {{
    border-bottom-color: var(--mc-accent);
}}

strong {{ font-weight: 700; }}
em {{ font-style: italic; }}
del {{ opacity: 0.6; }}

blockquote {{
    border-left: 4px solid var(--mc-accent);
    padding: 0.5em 1em;
    margin: 1em 0;
    background-color: var(--mc-code-bg);
    border-radius: 0 4px 4px 0;
}}

blockquote p {{ margin-bottom: 0; }}

pre {{
    background-color: var(--mc-code-bg);
    border: 1px solid var(--mc-border);
    border-radius: 6px;
    padding: 1em;
    overflow-x: auto;
    margin: 1em 0;
    font-size: 0.9em;
}}

code {{
    font-family: var(--mc-font-code);
    font-size: 0.9em;
}}

code.inline-code {{
    background-color: var(--mc-code-bg);
    padding: 0.15em 0.4em;
    border-radius: 3px;
    border: 1px solid var(--mc-border);
}}

pre code {{
    background: none;
    border: none;
    padding: 0;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
    font-size: 0.95em;
}}

th, td {{
    border: 1px solid var(--mc-border);
    padding: 0.6em 1em;
    text-align: left;
}}

th {{
    background-color: var(--mc-code-bg);
    font-weight: 600;
}}

tr:nth-child(even) {{
    background-color: var(--mc-code-bg);
}}

.table-wrapper {{
    overflow-x: auto;
    margin: 1em 0;
}}

ul, ol {{
    padding-left: 2em;
    margin-bottom: 1em;
}}

li {{
    margin-bottom: 0.3em;
}}

.task-list {{
    list-style: none;
    padding-left: 0;
}}

.task-item {{
    display: flex;
    align-items: flex-start;
    gap: 0.5em;
}}

.task-item input[type="checkbox"] {{
    margin-top: 0.4em;
    accent-color: var(--mc-accent);
}}

hr {{
    border: none;
    height: 2px;
    background-color: var(--mc-border);
    margin: 2em 0;
}}

figure {{
    margin: 1.5em 0;
    text-align: center;
}}

figure img {{
    max-width: 100%;
    height: auto;
    border-radius: 6px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}}

figcaption {{
    margin-top: 0.5em;
    font-size: 0.9em;
    color: var(--mc-fg);
    opacity: 0.7;
}}

/* 目录样式 */
.mc-toc {{
    background-color: var(--mc-code-bg);
    border: 1px solid var(--mc-border);
    border-radius: 8px;
    padding: 1em 1.5em;
    margin-bottom: 2em;
}}

.mc-toc h3 {{
    margin-top: 0;
    margin-bottom: 0.5em;
    font-size: 1.1em;
}}

.mc-toc ul {{
    list-style: none;
    padding-left: 0;
    margin-bottom: 0;
}}

.mc-toc li {{
    margin-bottom: 0.2em;
}}

.mc-toc a {{
    color: var(--mc-fg);
    opacity: 0.8;
    font-size: 0.95em;
}}

.mc-toc a:hover {{
    opacity: 1;
    color: var(--mc-accent);
}}

/* 页脚信息 */
.mc-footer {{
    margin-top: 3em;
    padding-top: 1em;
    border-top: 1px solid var(--mc-border);
    font-size: 0.85em;
    opacity: 0.6;
    text-align: center;
}}

/* 打印样式 */
@media print {{
    body {{ padding: 0; max-width: none; }}
    pre {{ page-break-inside: avoid; }}
    table {{ page-break-inside: avoid; }}
    h1, h2, h3 {{ page-break-after: avoid; }}
}}
"""

        if responsive:
            css += """
@media screen and (max-width: 768px) {
    body {
        padding: 1rem;
        font-size: 15px;
    }
    h1 { font-size: 1.6em; }
    h2 { font-size: 1.3em; }
    pre { font-size: 0.85em; padding: 0.8em; }
}
"""

        if custom_css:
            css += f"\n/* Custom CSS */\n{custom_css}\n"

        return css

    @classmethod
    def get_toc_html(cls, headings: List[Dict], title: str = "目录") -> str:
        """生成目录HTML"""
        if not headings:
            return ""

        items = []
        for h in headings:
            indent = "  " * (h['level'] - 1)
            items.append(f'{indent}<li><a href="#{h["anchor"]}">{h["text"]}</a></li>')

        return f"""<nav class="mc-toc">
<h3>📖 {title}</h3>
<ul>
{chr(10).join(items)}
</ul>
</nav>"""


class MarkCraftEngine:
    """
    MarkCraft Studio 核心引擎
    整合解析器、主题引擎，提供统一的转换接口
    """

    def __init__(self):
        self.parser = MarkdownParser()

    def convert(
        self,
        markdown_text: str,
        config: Optional[ExportConfig] = None
    ) -> ParseResult:
        """
        将Markdown转换为解析结果

        Args:
            markdown_text: Markdown原始文本
            config: 导出配置（可选）

        Returns:
            ParseResult: 解析结果
        """
        if config is None:
            config = ExportConfig()

        return self.parser.parse(markdown_text)

    def to_html(
        self,
        markdown_text: str,
        config: Optional[ExportConfig] = None
    ) -> str:
        """
        将Markdown转换为完整HTML文档

        Args:
            markdown_text: Markdown原始文本
            config: 导出配置

        Returns:
            str: 完整HTML文档字符串
        """
        if config is None:
            config = ExportConfig()

        result = self.convert(markdown_text, config)

        # 生成CSS
        css = ThemeEngine.get_css(
            theme=config.theme,
            custom_css=config.css_custom,
            responsive=config.responsive
        )

        # 生成目录
        toc_html = ""
        if config.include_toc:
            toc_title = "目录" if config.language.startswith("zh") else "Table of Contents"
            toc_html = ThemeEngine.get_toc_html(result.toc, toc_title)

        # 元数据
        title = config.title
        author = config.author
        if result.metadata.get('title'):
            title = result.metadata['title']
        if result.metadata.get('author'):
            author = result.metadata['author']

        # 统计信息
        stats = f"📝 {result.word_count} 字 · ⏱️ 约 {result.reading_time} 分钟阅读"

        html = f"""<!DOCTYPE html>
<html lang="{config.language}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="generator" content="MarkCraft Studio v{__import__('markcraft').__version__}">
    <title>{title}</title>
    <style>{css}</style>
</head>
<body>
    <article>
        <header>
            <h1>{title}</h1>
            {f'<p style="opacity:0.6;">作者：{author}</p>' if author else ''}
            <p class="mc-stats">{stats}</p>
        </header>
        {toc_html}
        <main>{result.html}</main>
        <footer class="mc-footer">
            <p>由 MarkCraft Studio 生成 · {__import__('markcraft').__version__}</p>
        </footer>
    </article>
</body>
</html>"""

        return html

    def to_html_fragment(
        self,
        markdown_text: str,
        config: Optional[ExportConfig] = None
    ) -> str:
        """
        将Markdown转换为HTML片段（不含完整文档结构）
        适合嵌入到已有页面中
        """
        if config is None:
            config = ExportConfig()
        result = self.convert(markdown_text, config)
        return result.html
