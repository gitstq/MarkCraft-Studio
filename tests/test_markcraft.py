# MarkCraft Studio 测试套件

import os
import sys
import unittest

# 确保可以导入markcraft模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestMarkdownParser(unittest.TestCase):
    """Markdown解析器测试"""

    def setUp(self):
        from markcraft.core.engine import MarkdownParser
        self.parser = MarkdownParser()

    def test_heading_parsing(self):
        """测试标题解析"""
        result = self.parser.parse("# Hello\n## World\n### Test")
        self.assertEqual(len(result.headings), 3)
        self.assertEqual(result.headings[0]['level'], 1)
        self.assertEqual(result.headings[0]['text'], 'Hello')

    def test_bold_and_italic(self):
        """测试粗体和斜体"""
        result = self.parser.parse("**bold** and *italic*")
        self.assertIn('<strong>bold</strong>', result.html)
        self.assertIn('<em>italic</em>', result.html)

    def test_code_block(self):
        """测试代码块"""
        result = self.parser.parse("```python\nprint('hello')\n```")
        self.assertIn('<pre><code class="language-python">', result.html)
        self.assertIn('print', result.html)

    def test_inline_code(self):
        """测试行内代码"""
        result = self.parser.parse("Use `print()` function")
        self.assertIn('<code class="inline-code">print()</code>', result.html)

    def test_link(self):
        """测试链接"""
        result = self.parser.parse("[GitHub](https://github.com)")
        self.assertIn('<a href="https://github.com"', result.html)

    def test_image(self):
        """测试图片"""
        result = self.parser.parse("![alt](image.png)")
        self.assertIn('<img src="image.png" alt="alt"', result.html)

    def test_blockquote(self):
        """测试引用块"""
        result = self.parser.parse("> This is a quote")
        self.assertIn('<blockquote>', result.html)

    def test_unordered_list(self):
        """测试无序列表"""
        result = self.parser.parse("- Item 1\n- Item 2\n- Item 3")
        self.assertIn('<ul>', result.html)
        self.assertIn('<li>Item 1</li>', result.html)

    def test_ordered_list(self):
        """测试有序列表"""
        result = self.parser.parse("1. First\n2. Second\n3. Third")
        self.assertIn('<ol>', result.html)
        self.assertIn('<li>First</li>', result.html)

    def test_table(self):
        """测试表格"""
        md = "| A | B |\n|---|---|\n| 1 | 2 |\n| 3 | 4 |"
        result = self.parser.parse(md)
        self.assertIn('<table>', result.html)
        self.assertIn('<th>A</th>', result.html)

    def test_horizontal_rule(self):
        """测试水平线"""
        result = self.parser.parse("---")
        self.assertIn('<hr>', result.html)

    def test_strikethrough(self):
        """测试删除线"""
        result = self.parser.parse("~~deleted~~")
        self.assertIn('<del>deleted</del>', result.html)

    def test_task_list(self):
        """测试任务列表"""
        result = self.parser.parse("- [x] Done\n- [ ] Todo")
        self.assertIn('type="checkbox"', result.html)
        self.assertIn('checked', result.html)

    def test_frontmatter(self):
        """测试YAML前置数据"""
        md = "---\ntitle: Test\ndate: 2026-01-01\n---\n# Hello"
        result = self.parser.parse(md)
        self.assertEqual(result.metadata.get('title'), 'Test')
        self.assertEqual(result.metadata.get('date'), '2026-01-01')

    def test_word_count(self):
        """测试字数统计"""
        result = self.parser.parse("Hello World 你好世界")
        self.assertGreater(result.word_count, 0)

    def test_reading_time(self):
        """测试阅读时间估算"""
        long_text = "测试文本" * 200
        result = self.parser.parse(long_text)
        self.assertGreaterEqual(result.reading_time, 1)

    def test_empty_input(self):
        """测试空输入"""
        result = self.parser.parse("")
        self.assertEqual(result.word_count, 0)
        self.assertEqual(len(result.headings), 0)


class TestThemeEngine(unittest.TestCase):
    """主题引擎测试"""

    def test_all_themes_generate_css(self):
        """测试所有主题都能生成CSS"""
        from markcraft.core.engine import ThemeEngine, ThemePreset
        for theme in ThemePreset:
            css = ThemeEngine.get_css(theme)
            self.assertIn(':root', css)
            self.assertIn('--mc-bg', css)
            self.assertGreater(len(css), 100)

    def test_custom_css(self):
        """测试自定义CSS"""
        from markcraft.core.engine import ThemeEngine, ThemePreset
        custom = "body { font-size: 20px; }"
        css = ThemeEngine.get_css(ThemePreset.MINIMAL, custom_css=custom)
        self.assertIn('font-size: 20px', css)

    def test_responsive_css(self):
        """测试响应式CSS"""
        from markcraft.core.engine import ThemeEngine, ThemePreset
        css = ThemeEngine.get_css(ThemePreset.MINIMAL, responsive=True)
        self.assertIn('@media', css)

    def test_toc_generation(self):
        """测试目录生成"""
        from markcraft.core.engine import ThemeEngine
        headings = [
            {'level': 1, 'text': 'Title', 'anchor': 'title'},
            {'level': 2, 'text': 'Section', 'anchor': 'section'},
        ]
        toc = ThemeEngine.get_toc_html(headings)
        self.assertIn('mc-toc', toc)
        self.assertIn('Title', toc)
        self.assertIn('Section', toc)

    def test_empty_toc(self):
        """测试空目录"""
        from markcraft.core.engine import ThemeEngine
        toc = ThemeEngine.get_toc_html([])
        self.assertEqual(toc, "")


class TestMarkCraftEngine(unittest.TestCase):
    """MarkCraft引擎集成测试"""

    def setUp(self):
        from markcraft.core.engine import MarkCraftEngine
        self.engine = MarkCraftEngine()

    def test_basic_conversion(self):
        """测试基本转换"""
        md = "# Hello\n\nWorld"
        result = self.engine.convert(md)
        self.assertIn('<h1', result.html)

    def test_full_html_output(self):
        """测试完整HTML输出"""
        md = "# Test\n\nContent"
        html = self.engine.to_html(md)
        self.assertIn('<!DOCTYPE html>', html)
        self.assertIn('<html', html)
        self.assertIn('</html>', html)

    def test_html_fragment(self):
        """测试HTML片段输出"""
        md = "**bold** text"
        fragment = self.engine.to_html_fragment(md)
        self.assertNotIn('<!DOCTYPE html>', fragment)
        self.assertIn('<strong>bold</strong>', fragment)

    def test_custom_config(self):
        """测试自定义配置"""
        from markcraft.core.engine import ExportConfig, ThemePreset
        config = ExportConfig(
            title="Custom Title",
            author="Test Author",
            theme=ThemePreset.DARK,
        )
        html = self.engine.to_html("# Test", config)
        self.assertIn('Custom Title', html)
        self.assertIn('Test Author', html)
        self.assertIn('--mc-bg: #1a1a2e', html)

    def test_complex_markdown(self):
        """测试复杂Markdown文档"""
        md = """---
title: 复杂文档
author: 测试
---

# 标题

## 第一节

正文内容

### 子节

- 列表项一
- 列表项二

> 引用内容

```python
def test():
    return 42
```

| 列1 | 列2 |
|-----|-----|
| A   | B   |

---

**粗体** *斜体* `代码` [链接](https://example.com)

- [x] 已完成
- [ ] 未完成
"""
        result = self.engine.convert(md)
        self.assertEqual(result.metadata.get('title'), '复杂文档')
        self.assertGreater(len(result.headings), 0)
        self.assertIn('<table>', result.html)
        self.assertIn('<blockquote>', result.html)
        self.assertIn('<pre><code', result.html)


class TestHelpers(unittest.TestCase):
    """工具函数测试"""

    def test_word_count(self):
        """测试字数统计"""
        from markcraft.utils.helpers import count_words
        self.assertEqual(count_words("Hello"), 1)
        self.assertEqual(count_words("你好世界"), 4)
        self.assertGreater(count_words("Hello 你好"), 0)

    def test_reading_time(self):
        """测试阅读时间"""
        from markcraft.utils.helpers import estimate_reading_time
        self.assertGreaterEqual(estimate_reading_time("短文本"), 1)

    def test_file_operations(self):
        """测试文件读写"""
        from markcraft.utils.helpers import read_file, write_file
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False, mode='w') as f:
            f.write("test content")
            temp_path = f.name

        try:
            content = read_file(temp_path)
            self.assertEqual(content, "test content")
        finally:
            os.unlink(temp_path)


class TestTemplates(unittest.TestCase):
    """模板系统测试"""

    def test_list_templates(self):
        """测试列出模板"""
        from markcraft.templates.builtins import list_templates
        templates = list_templates()
        self.assertIn('article', templates)
        self.assertIn('readme', templates)

    def test_get_template(self):
        """测试获取模板"""
        from markcraft.templates.builtins import get_template
        content = get_template('article')
        self.assertIn('#', content)
        self.assertIn('标题', content)

    def test_invalid_template(self):
        """测试无效模板"""
        from markcraft.templates.builtins import get_template
        with self.assertRaises(KeyError):
            get_template('nonexistent')


class TestExporters(unittest.TestCase):
    """导出器测试"""

    def setUp(self):
        from markcraft.core.engine import MarkCraftEngine, ExportConfig
        self.engine = MarkCraftEngine()
        self.config = ExportConfig()
        self.sample_md = "# Test Document\n\nThis is a test.\n\n## Section\n\nContent here."

    def test_html_export(self):
        """测试HTML导出"""
        from markcraft.exporters.html_exporter import HTMLExporter
        import tempfile
        exporter = HTMLExporter()
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as f:
            temp_path = f.name
        try:
            result = exporter.export(self.sample_md, temp_path, self.config, self.engine)
            self.assertTrue(os.path.exists(result))
            with open(result, 'r') as f:
                content = f.read()
            self.assertIn('<!DOCTYPE html>', content)
        finally:
            os.unlink(temp_path)

    def test_docx_export(self):
        """测试DOCX导出"""
        try:
            from docx import Document
        except ImportError:
            self.skipTest("python-docx not installed")
            return

        from markcraft.exporters.docx_exporter import DOCXExporter
        import tempfile
        exporter = DOCXExporter()
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as f:
            temp_path = f.name
        try:
            result = exporter.export(self.sample_md, temp_path, self.config, self.engine)
            self.assertTrue(os.path.exists(result))
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


if __name__ == '__main__':
    unittest.main()
