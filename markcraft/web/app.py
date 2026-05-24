"""
MarkCraft Studio Web 应用
提供可视化Markdown编辑和实时预览功能
"""

import os
from flask import Flask, render_template_string, request, jsonify, send_from_directory


def create_app(preview_content: str = None, preview_theme=None):
    """
    创建Flask应用实例

    Args:
        preview_content: 预览模式下的Markdown内容
        preview_theme: 预览模式下的主题
    """
    app = Flask(__name__)

    # HTML模板
    INDEX_HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MarkCraft Studio</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC", sans-serif; height: 100vh; display: flex; flex-direction: column; background: #1a1a2e; color: #e0e0e0; }
        .header { display: flex; align-items: center; justify-content: space-between; padding: 8px 16px; background: #16213e; border-bottom: 1px solid #0f3460; }
        .header h1 { font-size: 16px; font-weight: 600; }
        .header h1 span { color: #e94560; }
        .toolbar { display: flex; gap: 6px; align-items: center; }
        .toolbar button { padding: 4px 12px; border: 1px solid #0f3460; background: #16213e; color: #c9d1d9; border-radius: 4px; cursor: pointer; font-size: 12px; transition: all 0.2s; }
        .toolbar button:hover { background: #0f3460; color: #fff; }
        .toolbar button.active { background: #e94560; border-color: #e94560; color: #fff; }
        .toolbar select { padding: 4px 8px; border: 1px solid #0f3460; background: #16213e; color: #c9d1d9; border-radius: 4px; font-size: 12px; }
        .main { display: flex; flex: 1; overflow: hidden; }
        .editor-panel { flex: 1; display: flex; flex-direction: column; border-right: 1px solid #0f3460; }
        .preview-panel { flex: 1; overflow-y: auto; padding: 24px; background: #0d1117; }
        .editor-panel textarea { flex: 1; padding: 16px; border: none; background: #0d1117; color: #c9d1d9; font-family: "SF Mono", "Fira Code", "Noto Sans Mono", monospace; font-size: 14px; line-height: 1.6; resize: none; outline: none; }
        .editor-panel textarea::placeholder { color: #484f58; }
        .stats { padding: 4px 16px; background: #16213e; border-top: 1px solid #0f3460; font-size: 11px; color: #8b949e; display: flex; gap: 16px; }
        .preview-panel h1 { font-size: 2em; border-bottom: 2px solid #30363d; padding-bottom: 0.3em; margin-bottom: 0.5em; }
        .preview-panel h2 { font-size: 1.5em; border-bottom: 1px solid #30363d; padding-bottom: 0.2em; margin-top: 1.5em; }
        .preview-panel p { margin-bottom: 1em; line-height: 1.8; }
        .preview-panel a { color: #58a6ff; text-decoration: none; }
        .preview-panel a:hover { text-decoration: underline; }
        .preview-panel blockquote { border-left: 4px solid #e94560; padding: 0.5em 1em; margin: 1em 0; background: #161b22; border-radius: 0 4px 4px 0; }
        .preview-panel pre { background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 1em; overflow-x: auto; margin: 1em 0; }
        .preview-panel code { font-family: "SF Mono", "Fira Code", monospace; font-size: 0.9em; }
        .preview-panel code.inline-code { background: #161b22; padding: 0.15em 0.4em; border-radius: 3px; border: 1px solid #30363d; }
        .preview-panel table { width: 100%; border-collapse: collapse; margin: 1em 0; }
        .preview-panel th, .preview-panel td { border: 1px solid #30363d; padding: 0.6em 1em; text-align: left; }
        .preview-panel th { background: #161b22; }
        .preview-panel hr { border: none; height: 2px; background: #30363d; margin: 2em 0; }
        .preview-panel img { max-width: 100%; border-radius: 6px; }
        .preview-panel ul, .preview-panel ol { padding-left: 2em; margin-bottom: 1em; }
        .preview-panel .mc-toc { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 1em 1.5em; margin-bottom: 2em; }
        .preview-panel .mc-toc h3 { margin-top: 0; margin-bottom: 0.5em; font-size: 1.1em; border: none; padding: 0; }
        .preview-panel .mc-toc ul { list-style: none; padding-left: 0; }
        .preview-panel .mc-toc a { color: #c9d1d9; opacity: 0.8; }
        .preview-panel .mc-toc a:hover { color: #58a6ff; opacity: 1; }
        .toast { position: fixed; bottom: 20px; right: 20px; padding: 10px 20px; background: #e94560; color: #fff; border-radius: 6px; font-size: 13px; opacity: 0; transition: opacity 0.3s; pointer-events: none; }
        .toast.show { opacity: 1; }
        /* 主题覆盖 */
        .theme-minimal .preview-panel { background: #ffffff; }
        .theme-minimal .preview-panel, .theme-minimal .preview-panel h1, .theme-minimal .preview-panel h2, .theme-minimal .preview-panel p { color: #333; }
        .theme-elegant .preview-panel { background: #fefefe; }
        .theme-elegant .preview-panel, .theme-elegant .preview-panel h1, .theme-elegant .preview-panel h2, .theme-elegant .preview-panel p { color: #2c3e50; }
        .theme-warm .preview-panel { background: #fdf6e3; }
        .theme-warm .preview-panel, .theme-warm .preview-panel h1, .theme-warm .preview-panel h2, .theme-warm .preview-panel p { color: #657b83; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎨 MarkCraft <span>Studio</span></h1>
        <div class="toolbar">
            <select id="themeSelect">
                <option value="dark">🌙 暗黑</option>
                <option value="minimal">📄 极简</option>
                <option value="elegant">✨ 优雅</option>
                <option value="tech">💻 科技</option>
                <option value="warm">🌅 暖色</option>
            </select>
            <button onclick="exportHTML()">📥 导出HTML</button>
            <button onclick="copyHTML()">📋 复制HTML</button>
        </div>
    </div>
    <div class="main">
        <div class="editor-panel">
            <textarea id="editor" placeholder="在此输入Markdown内容...">{{ preview_content }}</textarea>
        </div>
        <div class="preview-panel" id="preview">
            <p style="opacity:0.5; text-align:center; margin-top:40vh;">在左侧输入Markdown内容，实时预览将在此显示...</p>
        </div>
    </div>
    <div class="stats">
        <span id="wordCount">📝 0 字</span>
        <span id="readTime">⏱️ 约 0 分钟</span>
        <span id="headingCount">📑 0 个标题</span>
    </div>
    <div class="toast" id="toast"></div>

    <script>
        const editor = document.getElementById('editor');
        const preview = document.getElementById('preview');
        const themeSelect = document.getElementById('themeSelect');
        let debounceTimer;

        editor.addEventListener('input', () => {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(updatePreview, 300);
        });

        themeSelect.addEventListener('change', () => {
            document.body.className = 'theme-' + themeSelect.value;
            updatePreview();
        });

        function updatePreview() {
            const content = editor.value;
            fetch('/api/convert', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    markdown: content,
                    theme: themeSelect.value,
                    include_toc: true
                })
            })
            .then(r => r.json())
            .then(data => {
                if (data.html) {
                    preview.innerHTML = data.html;
                }
                if (data.stats) {
                    document.getElementById('wordCount').textContent = '📝 ' + data.stats.word_count + ' 字';
                    document.getElementById('readTime').textContent = '⏱️ 约 ' + data.stats.reading_time + ' 分钟';
                    document.getElementById('headingCount').textContent = '📑 ' + data.stats.heading_count + ' 个标题';
                }
            })
            .catch(err => console.error('Preview error:', err));
        }

        function exportHTML() {
            const content = editor.value;
            if (!content.trim()) { showToast('请先输入内容'); return; }
            fetch('/api/export/html', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    markdown: content,
                    theme: themeSelect.value,
                    include_toc: true
                })
            })
            .then(r => r.blob())
            .then(blob => {
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'markcraft-export.html';
                a.click();
                URL.revokeObjectURL(url);
                showToast('✅ HTML导出成功！');
            });
        }

        function copyHTML() {
            const content = editor.value;
            if (!content.trim()) { showToast('请先输入内容'); return; }
            fetch('/api/convert', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    markdown: content,
                    theme: themeSelect.value,
                    include_toc: false
                })
            })
            .then(r => r.json())
            .then(data => {
                if (data.fragment) {
                    navigator.clipboard.writeText(data.fragment).then(() => {
                        showToast('✅ HTML片段已复制到剪贴板！');
                    });
                }
            });
        }

        function showToast(msg) {
            const toast = document.getElementById('toast');
            toast.textContent = msg;
            toast.classList.add('show');
            setTimeout(() => toast.classList.remove('show'), 2000);
        }

        // 初始加载
        {% if preview_content %}
            updatePreview();
        {% endif %}
    </script>
</body>
</html>"""

    @app.route('/')
    def index():
        return render_template_string(
            INDEX_HTML,
            preview_content=preview_content or ""
        )

    @app.route('/api/convert', methods=['POST'])
    def api_convert():
        """API: 将Markdown转换为HTML"""
        from markcraft.core.engine import MarkCraftEngine, ThemePreset, ExportConfig

        data = request.get_json()
        markdown_text = data.get('markdown', '')
        theme_name = data.get('theme', 'dark')
        include_toc = data.get('include_toc', True)

        theme_map = {
            'minimal': ThemePreset.MINIMAL,
            'elegant': ThemePreset.ELEGANT,
            'tech': ThemePreset.TECH,
            'warm': ThemePreset.WARM,
            'dark': ThemePreset.DARK,
        }

        engine = MarkCraftEngine()
        config = ExportConfig(
            theme=theme_map.get(theme_name, ThemePreset.DARK),
            include_toc=include_toc,
        )

        result = engine.convert(markdown_text, config)

        # 生成目录HTML
        toc_html = ""
        if include_toc and result.toc:
            from markcraft.core.engine import ThemeEngine
            toc_html = ThemeEngine.get_toc_html(result.toc)

        return jsonify({
            'html': toc_html + result.html,
            'fragment': result.html,
            'stats': {
                'word_count': result.word_count,
                'reading_time': result.reading_time,
                'heading_count': len(result.headings),
            }
        })

    @app.route('/api/export/html', methods=['POST'])
    def api_export_html():
        """API: 导出完整HTML文档"""
        from markcraft.core.engine import MarkCraftEngine, ThemePreset, ExportConfig

        data = request.get_json()
        markdown_text = data.get('markdown', '')
        theme_name = data.get('theme', 'dark')
        include_toc = data.get('include_toc', True)

        theme_map = {
            'minimal': ThemePreset.MINIMAL,
            'elegant': ThemePreset.ELEGANT,
            'tech': ThemePreset.TECH,
            'warm': ThemePreset.WARM,
            'dark': ThemePreset.DARK,
        }

        engine = MarkCraftEngine()
        config = ExportConfig(
            theme=theme_map.get(theme_name, ThemePreset.DARK),
            include_toc=include_toc,
        )

        html_content = engine.to_html(markdown_text, config)

        return app.response_class(
            response=html_content,
            status=200,
            mimetype='text/html'
        )

    return app
