#!/bin/bash
# =============================================================================
# 雨课堂下载器 (内嵌浏览器版) — 一键环境配置
# =============================================================================
# 安装所需依赖:
#   - PySide6 (包含 QtWebEngine, 自带 Chromium ~180MB)
#   - img2pdf, pillow 等 PDF 相关依赖
#
# 注意: QtWebEngine 下载量较大 (~200MB), 请保持网络通畅。
# =============================================================================

set -e

echo "============================================"
echo " 🌧 雨课堂下载器 (内嵌浏览器版) — 环境配置"
echo "============================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 未找到。请安装 Python 3.10+："
    echo "   https://www.python.org/downloads/"
    exit 1
fi

PYTHON=$(command -v python3)
echo "✅ Python: $($PYTHON --version)"

# Install deps
echo ""
echo "📦 正在安装 PySide6 (包含 QtWebEngine, ~200MB, 需要一些时间)..."
$PYTHON -m pip install --upgrade pip
$PYTHON -m pip install PySide6 img2pdf pillow pikepdf lxml pyinstaller

echo ""
echo "============================================"
echo " ✅ 环境配置完成！"
echo ""
echo " 使用方法："
echo "   python3 -m yuketang_downloader_embedded"
echo ""
echo " 浏览器内嵌在窗口中，无需额外安装 Chromium。"
echo "============================================"
