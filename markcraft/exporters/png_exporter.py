"""
PNG导出器
将Markdown转换为PNG图片
使用imgkit或Pillow进行截图
"""

import os
from markcraft.core.engine import MarkCraftEngine, ExportConfig


class PNGExporter:
    """PNG格式导出器"""

    def export(
        self,
        markdown_text: str,
        output_path: str,
        config: ExportConfig,
        engine: MarkCraftEngine
    ) -> str:
        """
        导出为PNG图片

        Args:
            markdown_text: Markdown原始文本
            output_path: 输出文件路径
            config: 导出配置
            engine: MarkCraft引擎实例

        Returns:
            str: 输出文件的完整路径
        """
        try:
            from PIL import Image, ImageDraw, ImageFont
        except ImportError:
            raise ImportError(
                "PNG导出需要安装Pillow库。请运行: pip install Pillow"
            )

        # 确保输出目录存在
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # 尝试使用imgkit（优先）
        try:
            import imgkit
            html_content = engine.to_html(markdown_text, config)

            # 临时HTML文件
            temp_html = output_path + '.temp.html'
            with open(temp_html, 'w', encoding='utf-8') as f:
                f.write(html_content)

            options = {
                'format': 'png',
                'width': config.width,
                'encoding': 'UTF-8',
                'enable-local-file-access': None,
            }

            imgkit.from_file(temp_html, output_path, options=options)

            # 清理临时文件
            if os.path.exists(temp_html):
                os.remove(temp_html)

            return os.path.abspath(output_path)

        except ImportError:
            pass
        except Exception:
            pass

        # 回退方案：使用Pillow生成简单的文本图片
        return self._export_with_pillow(markdown_text, output_path, config, engine)

    def _export_with_pillow(
        self,
        markdown_text: str,
        output_path: str,
        config: ExportConfig,
        engine: MarkCraftEngine
    ) -> str:
        """使用Pillow生成文本图片（回退方案）"""
        from PIL import Image, ImageDraw, ImageFont

        result = engine.convert(markdown_text, config)

        # 纯文本渲染
        text = result.html
        # 移除HTML标签
        import re
        text = re.sub(r'<[^>]+>', '\n', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = text.strip()

        # 配置
        width = config.width
        padding = 40
        font_size = 16
        line_height = font_size * 1.8

        # 获取主题颜色
        from markcraft.core.engine import ThemeEngine
        theme_colors = ThemeEngine.THEMES[config.theme]

        # 尝试加载中文字体
        font = None
        font_paths = [
            '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc',
            '/System/Library/Fonts/PingFang.ttc',
            'C:\\Windows\\Fonts\\msyh.ttc',
        ]
        for fp in font_paths:
            if os.path.exists(fp):
                try:
                    font = ImageFont.truetype(fp, font_size)
                    break
                except Exception:
                    continue

        if font is None:
            font = ImageFont.load_default()

        # 计算图片尺寸
        lines = text.split('\n')
        max_chars = (width - 2 * padding) // (font_size // 2)
        wrapped_lines = []
        for line in lines:
            if len(line) <= max_chars:
                wrapped_lines.append(line)
            else:
                for i in range(0, len(line), max_chars):
                    wrapped_lines.append(line[i:i + max_chars])

        img_height = padding * 2 + len(wrapped_lines) * int(line_height) + 60

        # 创建图片
        bg_color = theme_colors['bg']
        fg_color = theme_colors['fg']

        # 转换十六进制颜色
        bg_rgb = tuple(int(bg_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        fg_rgb = tuple(int(fg_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

        img = Image.new('RGB', (width, img_height), bg_rgb)
        draw = ImageDraw.Draw(img)

        # 绘制文本
        y = padding
        for line in wrapped_lines:
            draw.text((padding, y), line, fill=fg_rgb, font=font)
            y += int(line_height)

        # 添加水印
        watermark = f"MarkCraft Studio v{__import__('markcraft').__version__}"
        draw.text(
            (width - padding - len(watermark) * 6, img_height - 30),
            watermark,
            fill=(*fg_rgb[:3],),
            font=font
        )

        img.save(output_path, 'PNG')
        return os.path.abspath(output_path)
