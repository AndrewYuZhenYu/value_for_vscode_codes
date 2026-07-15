#!/bin/bash
# =============================================================================
# Rain Classroom Downloader — One-Click Setup
# =============================================================================
# Installs the dependencies needed to run the app:
#   1. Python packages (playwright, img2pdf, etc.)
#   2. Chromium browser for Playwright
#
# Usage:
#   chmod +x setup.sh
#   ./setup.sh
# =============================================================================

set -e

echo "============================================"
echo " 🚀 雨课堂课件下载器 — 环境配置"
echo "============================================"
echo ""

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 未找到。请先安装 Python 3.10+："
    echo "   https://www.python.org/downloads/"
    exit 1
fi

PYTHON=$(command -v python3)
echo "✅ Python: $($PYTHON --version)"

# Install Python dependencies
echo ""
echo "📦 正在安装 Python 依赖…"
$PYTHON -m pip install --upgrade pip
$PYTHON -m pip install playwright img2pdf pillow pikepdf lxml pyinstaller

# Install Chromium for Playwright
echo ""
echo "🌐 正在下载 Chromium 浏览器（约 340 MB，仅首次需要）…"
$PYTHON -m playwright install chromium

echo ""
echo "============================================"
echo " ✅ 环境配置完成！"
echo ""
echo " 使用方法："
echo "   1. 双击 'Rain Classroom Downloader.app' 启动"
echo "   2. 或者在终端运行："
echo "      python3 -m yuketang_downloader"
echo "============================================"
