"""
HTML导出器
将Markdown转换为格式化的HTML文档
"""

import os
from markcraft.core.engine import MarkCraftEngine, ExportConfig


class HTMLExporter:
    """HTML格式导出器"""

    def export(
        self,
        markdown_text: str,
        output_path: str,
        config: ExportConfig,
        engine: MarkCraftEngine
    ) -> str:
        """
        导出为HTML文件

        Args:
            markdown_text: Markdown原始文本
            output_path: 输出文件路径
            config: 导出配置
            engine: MarkCraft引擎实例

        Returns:
            str: 输出文件的完整路径
        """
        html_content = engine.to_html(markdown_text, config)

        # 确保输出目录存在
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return os.path.abspath(output_path)
