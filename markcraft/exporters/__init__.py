"""
MarkCraft Studio 导出器模块
支持HTML、PDF、DOCX、PNG等多种格式导出
"""

from markcraft.core.engine import MarkCraftEngine, ExportConfig, OutputFormat
from markcraft.exporters.html_exporter import HTMLExporter
from markcraft.exporters.pdf_exporter import PDFExporter
from markcraft.exporters.docx_exporter import DOCXExporter
from markcraft.exporters.png_exporter import PNGExporter


class ExportManager:
    """
    导出管理器
    统一管理所有格式的导出操作
    """

    def __init__(self):
        self.engine = MarkCraftEngine()
        self._exporters = {
            OutputFormat.HTML: HTMLExporter(),
            OutputFormat.PDF: PDFExporter(),
            OutputFormat.DOCX: DOCXExporter(),
            OutputFormat.PNG: PNGExporter(),
        }

    def export(
        self,
        markdown_text: str,
        output_path: str,
        config: ExportConfig = None
    ) -> str:
        """
        导出Markdown到指定格式

        Args:
            markdown_text: Markdown原始文本
            output_path: 输出文件路径
            config: 导出配置

        Returns:
            str: 导出文件的完整路径
        """
        if config is None:
            config = ExportConfig()

        # 根据文件扩展名推断格式
        ext = output_path.rsplit('.', 1)[-1].lower() if '.' in output_path else ''
        format_map = {
            'html': OutputFormat.HTML,
            'htm': OutputFormat.HTML,
            'pdf': OutputFormat.PDF,
            'docx': OutputFormat.DOCX,
            'png': OutputFormat.PNG,
            'jpg': OutputFormat.PNG,
            'jpeg': OutputFormat.PNG,
        }

        if ext in format_map:
            config.format = format_map[ext]

        exporter = self._exporters.get(config.format)
        if exporter is None:
            raise ValueError(f"Unsupported export format: {config.format}")

        return exporter.export(markdown_text, output_path, config, self.engine)

    def export_all(
        self,
        markdown_text: str,
        output_dir: str,
        base_name: str,
        config: ExportConfig = None
    ) -> dict:
        """
        一次性导出所有支持的格式

        Args:
            markdown_text: Markdown原始文本
            output_dir: 输出目录
            base_name: 基础文件名（不含扩展名）
            config: 导出配置

        Returns:
            dict: 各格式的输出路径
        """
        import os
        os.makedirs(output_dir, exist_ok=True)

        if config is None:
            config = ExportConfig()

        results = {}
        for fmt, exporter in self._exporters.items():
            ext_map = {
                OutputFormat.HTML: 'html',
                OutputFormat.PDF: 'pdf',
                OutputFormat.DOCX: 'docx',
                OutputFormat.PNG: 'png',
            }
            output_path = os.path.join(output_dir, f"{base_name}.{ext_map[fmt]}")
            try:
                results[fmt.value] = exporter.export(
                    markdown_text, output_path, config, self.engine
                )
            except Exception as e:
                results[fmt.value] = f"Error: {str(e)}"

        return results
