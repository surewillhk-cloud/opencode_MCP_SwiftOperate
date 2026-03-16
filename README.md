# LLM Agent Team

LLM 驱动的 Agent 开发团队，支持动态模型选择和并行执行。

## 启动 Logo

```
  ____                       _     _   _ 
 / ___| _ __ ___   __ _ _ __| |_  | | | |
 \___ \| '_ ` _ \ / _` | '__| __| | | | |
  ___) | | | | | | (_| | |  | |_  | |_| |
 |____/|_| |_| |_|\__,_|_|   \__|  \___/ 
 
  🟡 LLM Agent Team  v1.0
  Dynamic Model | Parallel Exec | Auto-Security
```

## 目录结构

```
opencode_MCP_SwiftOperate/
├── .ai-team/                   # 核心代码
│   ├── config/                 # 配置文件
│   │   └── agents.yaml         # Agent 和工作流配置
│   ├── src/                   # 源代码
│   │   ├── core/               # 核心模块
│   │   ├── agents/             # Agent 基类
│   │   └── utils/              # 工具函数
│   │       └── banner.py        # Logo 打印
│   └── opencode-agent-skill/   # Agent 和 Skill 定义
│       └── .opencode/
│           ├── agent/           # 7 个 Agent prompt
│           └── skills/          # 21 个 Skill
├── AGENTS.md                   # 系统配置文档
└── README.md                    # 说明文档
```

## 快速开始

### 1. 安装依赖

```bash
cd ./.ai-team
pip install -r requirements.txt
```

### 2. 配置 MCP

编辑 `~/.mcp/agent-team.json`，确保路径正确：

```json
{
  "mcpServers": {
    "agent-team": {
      "command": "python3",
      "args": ["./ai-team/mcp_server.py"],
      "env": {}
    }
  }
}
```

### 3. 启动

1. 打开 OpenCode（或 Claude Code）
2. 系统自动加载 MCP 配置
3. 启动时显示 Logo 和 Agent 列表

## 使用方式

### OpenCode / Claude Code

启动 OpenCode 后，系统自动加载 MCP 配置，显示：

```
  ____                       _     _   _ 
 / ___| _ __ ___   __ _ _ __| |_  | | | |
 \___ \| '_ ` _ \ / _` | '__| __| | | | |
  ___) | | | | | | (_| | |  | |_  | |_| |
 |____/|_| |_| |_|\__,_|_|   \__|  \___/ 
 
  🟡 LLM Agent Team  v1.0
  Dynamic Model | Parallel Exec | Auto-Security
```

然后直接输入开发需求即可。

### 备用：直接运行

```bash
cd ./.ai-team
python3 main.py "开发一个 todo app"
```

### MCP Server (OpenCode / Claude Code)

MCP Server 已自动配置，重启 OpenCode 即可使用。

**可用工具：**
- `execute_workflow` - 执行工作流
- `list_workflows` - 列出工作流
- `list_agents` - 列出 Agent
- `analyze_complexity` - 分析复杂度

## 核心功能

### 1. 动态模型选择

根据任务复杂度自动选择合适的模型：

| 复杂度 | 适用场景 | 示例 |
|--------|----------|------|
| low | 简单页面 | landing page |
| medium | 中等复杂度 | 登录系统、CURD |
| high | 复杂系统 | ERP、电商 |
| advanced | 企业级 | DeFi、SaaS |

### 2. 并行执行

支持并行执行多个 Agent：

```
quick_dev:  [architect] → [frontend-dev + backend-dev] → [guardian]
                    ↓                    ↓
                串行              并行执行
```

### 3. 并发调研

architect Agent 启动时会自动并发搜索：
- Web 搜索（Serper API / 免费搜索）
- GitHub 代码仓库
- 官方文档

### 4. 配置引导

启动时自动检测 API 配置：
- 有 API → 使用第三方模型
- 无 API → 使用当前 AI 直接执行

## Agents (7)

| Agent | 职责 |
|-------|------|
| architect | 需求分析、任务分发、并发调研 |
| ui-prompt | UI 提示词工程 |
| ui-generator | UI 可视化生成 |
| frontend-dev | 前端开发 |
| backend-dev | 后端开发 |
| guardian | 质量守护 (QA+安全) |
| operator | DevOps 运维 |

## 工作流

| 工作流 | 说明 | 步骤 |
|--------|------|-------|
| full_product | 完整产品开发 | architect → ui-prompt → ui-generator → frontend → backend → guardian |
| quick_dev | 快速开发（并行） | [architect] → [frontend + backend] → [guardian] |
| frontend_only | 仅前端 | architect → ui-prompt → frontend → guardian |
| backend_only | 仅后端 | architect → backend → guardian |
| ui_design | UI 设计 | architect → ui-prompt → ui-generator |
| deployment | 部署 | operator → guardian |

## MCP 配置

MCP 配置文件位置：`~/.mcp/agent-team.json`

```json
{
  "mcpServers": {
    "agent-team": {
      "command": "python3",
      "args": ["./ai-team/mcp_server.py"],
      "env": {}
    }
  }
}
```

## 复制到新环境

```bash
# 1. 复制文件夹
cp -r ./opencode_MCP_SwiftOperate /新项目目录/

# 2. 安装依赖
cd /新项目目录/opencode_MCP_SwiftOperate/.ai-team
pip install -r requirements.txt

# 3. 配置 MCP
# 编辑 ~/.mcp/agent-team.json，修改路径为新路径

# 4. 启动 OpenCode
# 系统自动加载 MCP
```
