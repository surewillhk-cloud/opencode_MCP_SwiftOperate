#!/bin/bash
#
# LLM Agent Team 安装脚本
# 
# 使用方法:
#   ./install.sh              # 交互式安装
#   ./install.sh --auto      # 自动安装（使用默认配置）
#   ./install.sh --mcp       # 仅安装 MCP Server
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "============================================"
echo "  LLM Agent Team 安装脚本"
echo "============================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python 3"
    echo "   请先安装 Python 3.10+"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Python 版本: $PYTHON_VERSION"

# 检查 pip
if ! command -v pip3 &> /dev/null && ! python3 -m pip --version &> /dev/null; then
    echo "❌ 错误: 未找到 pip"
    exit 1
fi

echo "✓ pip 已安装"

# 安装依赖
echo ""
echo "📦 安装 Python 依赖..."
python3 -m pip install -r requirements.txt --quiet
echo "✓ 依赖安装完成"

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo ""
    echo "📝 配置文件..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✓ 已创建 .env 文件"
        echo ""
        echo "⚠️  请编辑 .env 文件填入你的 API Key:"
        echo "   OPENROUTER_API_KEY=你的密钥"
    else
        echo "❌ 错误: 未找到 .env.example"
        exit 1
    fi
else
    echo "✓ .env 已存在"
fi

# 检查 MCP 配置目录
MCP_DIR="$HOME/.mcp"
if [ ! -d "$MCP_DIR" ]; then
    mkdir -p "$MCP_DIR"
fi

# 创建 MCP 配置
MCP_CONFIG_FILE="$MCP_DIR/agent-team.json"

echo ""
echo "🔧 配置 MCP Server..."

# 获取当前目录的绝对路径
ABSOLUTE_PATH="$(cd "$SCRIPT_DIR" && pwd)"

cat > "$MCP_CONFIG_FILE" << EOF
{
  "mcpServers": {
    "agent-team": {
      "command": "python3",
      "args": ["$ABSOLUTE_PATH/mcp_server.py"],
      "env": {}
    }
  }
}
EOF

echo "✓ MCP 配置已创建: $MCP_CONFIG_FILE"
echo ""
echo "============================================"
echo "  安装完成!"
echo "============================================"
echo ""
echo "📋 使用方法:"
echo ""
echo "1. 在 Claude Code / OpenCode 中使用:"
echo "   - 重启 Claude Code"
echo "   - MCP Server 会自动加载"
echo ""
echo "2. 直接运行:"
echo "   python3 main.py \"你的任务\" -w quick_dev --auto"
echo ""
echo "3. MCP 工具列表:"
echo "   - execute_workflow: 执行工作流"
echo "   - list_workflows: 列出工作流"
echo "   - list_agents: 列出 Agent"
echo "   - analyze_complexity: 分析复杂度"
echo "   - select_models: 选择模型"
echo "   - estimate_cost: 估算成本"
echo ""
echo "============================================"
