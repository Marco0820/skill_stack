#!/bin/bash
# anthropics/skills 一键安装脚本
# 用法：bash install_anthropics_skills.sh

set -e

echo "=========================================="
echo "  anthropics/skills 技能安装脚本"
echo "=========================================="
echo ""

# 检查是否已安装
if [ -d "$HOME/.claude/skills/anthropics-skills" ]; then
    echo "⚠️  检测到 anthropics-skills 目录已存在"
    read -p "是否重新安装？(y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "取消安装"
        exit 0
    fi
    echo "删除旧目录..."
    rm -rf "$HOME/.claude/skills/anthropics-skills"
fi

# 克隆仓库
echo "📥 正在克隆 anthropics/skills 仓库..."
git clone --depth 1 https://github.com/anthropics/skills.git "$HOME/.claude/skills/anthropics-skills"

# 进入目录
cd "$HOME/.claude/skills/anthropics-skills"

# 检查Python
echo ""
echo "🐍 检查Python环境..."
if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo "❌ 未找到Python，请先安装Python3"
    exit 1
fi

echo "找到Python: $($PYTHON --version)"

# 安装依赖
echo ""
echo "📦 安装Python依赖..."
$PYTHON -m pip install --upgrade pip
$PYTHON -m pip install pypdf python-docx openpyxl python-pptx

# 列出可用技能
echo ""
echo "✅ 安装完成！"
echo ""
echo "可用的技能："
echo ""
echo "📄 文档处理："
ls -d skills/pdf skills/docx skills/xlsx skills/pptx 2>/dev/null | xargs -I {} basename {}
echo ""
echo "🎨 创意设计："
ls -d skills/algorithmic-art skills/canvas-design skills/frontend-design skills/theme-factory 2>/dev/null | xargs -I {} basename {}
echo ""
echo "💼 企业应用："
ls -d skills/brand-guidelines skills/internal-comms skills/slack-gif-creator 2>/dev/null | xargs -I {} basename {}
echo ""
echo "🔧 开发工具："
ls -d skills/claude-api skills/mcp-builder skills/skill-creator skills/webapp-testing 2>/dev/null | xargs -I {} basename {}
echo ""
echo "=========================================="
echo "  安装完成！请重启 Claude Code 使用"
echo "=========================================="
