"""
PDF导出器
将Markdown转换为PDF文档
使用WeasyPrint进行高质量PDF渲染
"""

import os
from markcraft.core.engine import MarkCraftEngine, ExportConfig


class PDFExporter:
    """PDF格式导出器"""

    def export(
        self,
        markdown_text: str,
        output_path: str,
        config: ExportConfig,
        engine: MarkCraftEngine
    ) -> str:
        """
        导出为PDF文件

        Args:
            markdown_text: Markdown原始文本
            output_path: 输出文件路径
            config: 导出配置
            engine: MarkCraft引擎实例

        Returns:
            str: 输出文件的完整路径
        """
        try:
            from weasyprint import HTML
        except ImportError:
            raise ImportError(
                "PDF导出需要安装weasyprint库。请运行: pip install weasyprint"
            )

        html_content = engine.to_html(markdown_text, config)

        # 确保输出目录存在
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # 使用WeasyPrint渲染PDF
        html_doc = HTML(string=html_content)
        html_doc.write_pdf(
            output_path,
            presentational_hints=True
        )

        return os.path.abspath(output_path)
