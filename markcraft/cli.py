"""
MarkCraft Studio CLI 命令行接口
提供终端快速操作Markdown/HTML转换的能力
"""

import argparse
import sys
import os


def create_parser() -> argparse.ArgumentParser:
    """创建CLI参数解析器"""
    parser = argparse.ArgumentParser(
        prog='markcraft',
        description='🎨 MarkCraft Studio - AI驱动的轻量级Markdown/HTML智能编辑与多平台发布引擎',
        epilog='示例: markcraft convert input.md -f html -o output.html --theme elegant',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # convert 命令
    convert_parser = subparsers.add_parser(
        'convert',
        help='转换Markdown文件为指定格式',
        description='将Markdown文件转换为HTML、PDF、DOCX或PNG格式'
    )
    convert_parser.add_argument(
        'input',
        help='输入Markdown文件路径'
    )
    convert_parser.add_argument(
        '-o', '--output',
        help='输出文件路径（默认与输入文件同目录）'
    )
    convert_parser.add_argument(
        '-f', '--format',
        choices=['html', 'pdf', 'docx', 'png', 'all'],
        default='html',
        help='输出格式（默认: html）'
    )
    convert_parser.add_argument(
        '-t', '--theme',
        choices=['minimal', 'elegant', 'tech', 'warm', 'dark'],
        default='elegant',
        help='主题风格（默认: elegant）'
    )
    convert_parser.add_argument(
        '--title',
        help='文档标题（默认从文件名或YAML前置数据提取）'
    )
    convert_parser.add_argument(
        '--author',
        help='文档作者'
    )
    convert_parser.add_argument(
        '--lang',
        default='zh-CN',
        help='文档语言（默认: zh-CN）'
    )
    convert_parser.add_argument(
        '--no-toc',
        action='store_true',
        help='不生成目录'
    )
    convert_parser.add_argument(
        '--css',
        help='自定义CSS文件路径'
    )
    convert_parser.add_argument(
        '--width',
        type=int,
        default=1200,
        help='PNG输出宽度（默认: 1200）'
    )

    # serve 命令
    serve_parser = subparsers.add_parser(
        'serve',
        help='启动Web可视化编辑服务器',
        description='启动本地Web服务器，提供可视化Markdown编辑和预览功能'
    )
    serve_parser.add_argument(
        '-p', '--port',
        type=int,
        default=8765,
        help='服务端口（默认: 8765）'
    )
    serve_parser.add_argument(
        '-H', '--host',
        default='127.0.0.1',
        help='绑定地址（默认: 127.0.0.1）'
    )
    serve_parser.add_argument(
        '--no-browser',
        action='store_true',
        help='不自动打开浏览器'
    )

    # preview 命令
    preview_parser = subparsers.add_parser(
        'preview',
        help='快速预览Markdown文件',
        description='在浏览器中快速预览Markdown文件的渲染效果'
    )
    preview_parser.add_argument(
        'input',
        help='输入Markdown文件路径'
    )
    preview_parser.add_argument(
        '-t', '--theme',
        choices=['minimal', 'elegant', 'tech', 'warm', 'dark'],
        default='elegant',
        help='主题风格（默认: elegant）'
    )
    preview_parser.add_argument(
        '-p', '--port',
        type=int,
        default=8766,
        help='预览服务端口（默认: 8766）'
    )

    # themes 命令
    themes_parser = subparsers.add_parser(
        'themes',
        help='查看可用主题列表',
        description='列出所有可用的主题预设及其说明'
    )

    # version 命令
    version_parser = subparsers.add_parser(
        'version',
        help='查看版本信息'
    )

    return parser


def cmd_convert(args):
    """执行转换命令"""
    from markcraft.core.engine import ExportConfig, ThemePreset, OutputFormat
    from markcraft.exporters import ExportManager

    # 读取输入文件
    if not os.path.exists(args.input):
        print(f"❌ 错误：文件不存在 - {args.input}")
        sys.exit(1)

    with open(args.input, 'r', encoding='utf-8') as f:
        markdown_text = f.read()

    # 构建配置
    theme_map = {
        'minimal': ThemePreset.MINIMAL,
        'elegant': ThemePreset.ELEGANT,
        'tech': ThemePreset.TECH,
        'warm': ThemePreset.WARM,
        'dark': ThemePreset.DARK,
    }

    custom_css = ""
    if args.css:
        if os.path.exists(args.css):
            with open(args.css, 'r', encoding='utf-8') as f:
                custom_css = f.read()
        else:
            print(f"⚠️ 警告：CSS文件不存在 - {args.css}")

    title = args.title or os.path.splitext(os.path.basename(args.input))[0]

    config = ExportConfig(
        theme=theme_map[args.theme],
        title=title,
        author=args.author or "",
        language=args.lang,
        css_custom=custom_css,
        include_toc=not args.no_toc,
        width=args.width,
    )

    manager = ExportManager()

    if args.format == 'all':
        # 导出所有格式
        base_name = os.path.splitext(os.path.basename(args.input))[0]
        output_dir = os.path.dirname(args.output) if args.output else os.path.dirname(args.input) or '.'
        results = manager.export_all(markdown_text, output_dir, base_name, config)

        print(f"\n✅ 批量导出完成！")
        print(f"📁 输出目录：{os.path.abspath(output_dir)}")
        for fmt, path in results.items():
            status = "✅" if not path.startswith("Error") else "❌"
            print(f"  {status} {fmt}: {path}")
    else:
        # 单格式导出
        if args.output:
            output_path = args.output
        else:
            base_name = os.path.splitext(os.path.basename(args.input))[0]
            output_path = os.path.join(
                os.path.dirname(args.input) or '.',
                f"{base_name}.{args.format}"
            )

        format_map = {
            'html': OutputFormat.HTML,
            'pdf': OutputFormat.PDF,
            'docx': OutputFormat.DOCX,
            'png': OutputFormat.PNG,
        }
        config.format = format_map[args.format]

        try:
            result_path = manager.export(markdown_text, output_path, config)
            print(f"\n✅ 转换成功！")
            print(f"📄 输出文件：{result_path}")
            print(f"🎨 主题：{args.theme}")
            print(f"📐 格式：{args.format.upper()}")
        except Exception as e:
            print(f"\n❌ 转换失败：{str(e)}")
            sys.exit(1)


def cmd_serve(args):
    """启动Web服务器"""
    try:
        from markcraft.web.app import create_app
    except ImportError:
        print("❌ Web服务需要安装Flask。请运行: pip install flask")
        sys.exit(1)

    app = create_app()
    print(f"\n🎨 MarkCraft Studio Web 编辑器已启动")
    print(f"🌐 访问地址：http://{args.host}:{args.port}")
    print(f"按 Ctrl+C 停止服务\n")

    if not args.no_browser:
        import webbrowser
        import threading
        def open_browser():
            import time
            time.sleep(1)
            webbrowser.open(f'http://{args.host}:{args.port}')
        threading.Thread(target=open_browser, daemon=True).start()

    app.run(host=args.host, port=args.port, debug=False)


def cmd_preview(args):
    """快速预览Markdown文件"""
    try:
        from markcraft.web.app import create_app
    except ImportError:
        print("❌ 预览功能需要安装Flask。请运行: pip install flask")
        sys.exit(1)

    if not os.path.exists(args.input):
        print(f"❌ 错误：文件不存在 - {args.input}")
        sys.exit(1)

    with open(args.input, 'r', encoding='utf-8') as f:
        markdown_text = f.read()

    from markcraft.core.engine import ThemePreset
    theme_map = {
        'minimal': ThemePreset.MINIMAL,
        'elegant': ThemePreset.ELEGANT,
        'tech': ThemePreset.TECH,
        'warm': ThemePreset.WARM,
        'dark': ThemePreset.DARK,
    }

    app = create_app(
        preview_content=markdown_text,
        preview_theme=theme_map[args.theme]
    )

    print(f"\n🎨 MarkCraft Studio 预览模式")
    print(f"🌐 预览地址：http://127.0.0.1:{args.port}")
    print(f"📄 文件：{args.input}")
    print(f"🎨 主题：{args.theme}")
    print(f"按 Ctrl+C 关闭预览\n")

    import webbrowser
    import threading
    def open_browser():
        import time
        time.sleep(1)
        webbrowser.open(f'http://127.0.0.1:{args.port}')
    threading.Thread(target=open_browser, daemon=True).start()

    app.run(host='127.0.0.1', port=args.port, debug=False)


def cmd_themes(args):
    """显示可用主题"""
    from markcraft.core.engine import ThemeEngine

    print("\n🎨 MarkCraft Studio 可用主题\n")
    print(f"{'主题':<12} {'标识':<12} {'说明'}")
    print("─" * 50)

    for preset, colors in ThemeEngine.THEMES.items():
        print(f"{colors['name']:<10} {preset.value:<12} 背景色: {colors['bg']} | 强调色: {colors['accent']}")

    print(f"\n💡 使用方法: markcraft convert input.md -t {ThemePreset.ELEGANT.value}")
    print()


def cmd_version(args):
    """显示版本信息"""
    from markcraft import __version__
    print(f"\n🎨 MarkCraft Studio v{__version__}")
    print("AI驱动的轻量级Markdown/HTML智能编辑与多平台发布引擎")
    print("MIT License | https://github.com/gitstq/MarkCraft-Studio\n")


def main():
    """CLI入口"""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    command_map = {
        'convert': cmd_convert,
        'serve': cmd_serve,
        'preview': cmd_preview,
        'themes': cmd_themes,
        'version': cmd_version,
    }

    handler = command_map.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
