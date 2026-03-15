#!/bin/bash
#
# LLM Agent Team 开发脚本
#
# 使用方法:
#   ./dev.sh "任务描述"              # 使用默认工作流 (quick_dev)
#   ./dev.sh "任务描述" -w full_product  # 指定工作流
#   ./dev.sh --list                  # 列出所有工作流
#   ./dev.sh --agents                # 列出所有 Agent
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 默认工作流
WORKFLOW="quick_dev"
AUTO=true

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -w|--workflow)
            WORKFLOW="$2"
            shift 2
            ;;
        -a|--auto)
            AUTO="$2"
            shift 2
            ;;
        --list)
            python3 main.py --list-workflows
            exit 0
            ;;
        --agents)
            python3 main.py --list-agents
            exit 0
            ;;
        --no-auto)
            AUTO=false
            shift
            ;;
        -h|--help)
            echo "使用方法: $0 \"任务描述\" [-w 工作流]"
            echo ""
            echo "选项:"
            echo "  -w, --workflow    指定工作流 (默认: quick_dev)"
            echo "  --list            列出所有工作流"
            echo "  --agents          列出所有 Agent"
            echo "  --no-auto         禁用自动确认"
            echo "  -h, --help        显示帮助"
            exit 0
            ;;
        *)
            TASK="$1"
            shift
            ;;
    esac
done

if [ -z "$TASK" ]; then
    echo "错误: 请提供任务描述"
    echo "使用方法: $0 \"任务描述\" [-w 工作流]"
    exit 1
fi

# 执行任务
if [ "$AUTO" = "false" ]; then
    python3 main.py "$TASK" -w "$WORKFLOW"
else
    python3 main.py "$TASK" -w "$WORKFLOW" --auto
fi
