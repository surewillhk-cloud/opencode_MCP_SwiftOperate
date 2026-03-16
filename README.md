# LLM Agent Team

LLM 驱动的 Agent 开发团队，支持动态模型选择和并行执行。

## 启动 Logo

```
  ____                       _     _   _ 
 / ___| _ __ ___   __ _ _ __| |_  | | | |
 \___ \| '_ ` _ \ / _` | '__| __| | | | |
  ___) | | | | | (_| | |  | |_  | |_| |
 |____/|_| |_| |_|\__,_|_|   \__| \___/  
 
  🟡 LLM Agent Team  v1.0
  Dynamic Model | Parallel Exec | Auto-Security
```

---

## 快速开始（傻瓜式操作）

### 步骤 1：启动 OpenCode

打开终端，输入：

```bash
opencode /path/to/opencode_MCP_SwiftOperate
```

> 💡 提示：将文件夹拖入终端即可自动显示路径

### 步骤 2：初始化

启动后，输入 `开始` 或 `start`，系统会自动检测 API 配置。

---

## 两种模式详解

### 模式一：有外部 API Key（如 OpenRouter）

当你配置了有效的 API Key 时，系统会调用外部 LLM 执行任务。

#### 配置 API Key

编辑 `.env` 文件：

```bash
cd ./.ai-team
cp .env.example .env
# 然后编辑 .env，填入你的 API Key
```

推荐使用 **OpenRouter**（支持多种模型）：

```
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxx
```

#### 使用方式

1. 启动 OpenCode
2. 输入你的需求，例如：`开发一个 todo app`
3. 系统自动选择合适的 Agent 执行
4. 工作流自动流转，直到完成

#### 动态模型选择

系统会根据任务复杂度自动选择模型：

| 复杂度 | 适用场景 | 模型 |
|--------|----------|------|
| low | 简单页面 | gemini-flash |
| medium | 登录系统、CURD | gemini-pro |
| high | ERP、电商 | claude-sonnet |
| advanced | DeFi、SaaS | gpt-5.4 |

---

### 模式二：无 API Key（Native Mode）

当没有配置有效的 API Key 时，系统使用**当前运行的 AI（你）**直接执行任务。

#### 特点

- ✅ 无需 API Key
- ✅ 使用当前 AI 的能力
- ⚠️ 每个阶段完成后需要你确认才能继续
- ⚠️ 建议先呼出对应的 Agent 角色再执行任务

#### 使用方式

1. 启动 OpenCode
2. 输入 `开始`
3. 系统显示配置引导，选择"没有 API Key"

```
【⚙️ API 配置检查】

我检测到你的 .env 还没有配置有效的 API Key。

请选择：
1. 提供 API Key，我帮你配置
2. 回复"没有"，我将使用当前 AI 直接执行任务
```

4. 输入你的需求，例如：`开发一个 todo app`

#### Native Mode 工作流程

```
用户: 开发一个 todo app

AI:
【第一阶段 - Architect】
我理解你的需求：开发一个简单的 Todo 应用。

【实现方案】
- 技术栈：React + Node.js
- 功能：添加、删除、标记完成
- 预计时间：30 分钟

[此时暂停，等待确认]
用户: 继续

AI:
【第二阶段 - Frontend + Backend】
[开始编写前端和后端代码]

[此时暂停，等待确认]
用户: 继续

AI:
【第三阶段 - Guardian】
[运行测试，检查代码质量]

完成！
```

#### 关键提示

⚠️ **每个阶段都需要确认**：当看到 "✅ 已完成 xxx，等待确认继续..." 时，输入"继续"或"下一步"才能进入下一阶段。

⚠️ **建议先呼出 Agent 角色**：对于复杂任务，可以先告诉 AI 你要扮演的角色，例如：
- "现在你扮演 frontend-dev agent，帮我写一个登录页面"
- "现在你扮演测试工程师，帮我验证这段代码"

---

## MCP 配置

如果 OpenCode 没有自动加载 MCP，手动配置：

### 方法一：复制配置文件

```bash
mkdir -p ~/.mcp
cp ./opencode_MCP_SwiftOperate/opencode.json ~/.mcp/agent-team.json
```

### 方法二：手动创建

编辑 `~/.mcp/agent-team.json`：

```json
{
  "mcpServers": {
    "agent-team": {
      "command": "python3",
      "args": ["./opencode_MCP_SwiftOperate/.ai-team/mcp_server.py"],
      "env": {}
    }
  }
}
```

---

## 可用工具

通过 MCP 调用以下工具：

| 工具 | 说明 |
|------|------|
| `execute_workflow` | 执行完整工作流 |
| `continue_workflow` | Native Mode 下继续工作流 |
| `execute_agent` | 调用单个 Agent |
| `list_workflows` | 列出所有工作流 |
| `list_agents` | 列出所有 Agent |
| `analyze_complexity` | 分析项目复杂度 |

---

## 工作流

| 工作流 | 说明 | 步骤 |
|--------|------|------|
| full_product | 完整产品开发 | architect → ui-prompt → ui-generator → frontend → backend → guardian |
| quick_dev | 快速开发（并行） | [architect] → [frontend + backend] → [guardian] |
| frontend_only | 仅前端 | architect → ui-prompt → frontend → guardian |
| backend_only | 仅后端 | architect → backend → guardian |
| ui_design | UI 设计 | architect → ui-prompt → ui-generator |
| deployment | 部署 | operator → guardian |

---

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

---

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
│   └── opencode-agent-skill/   # Agent 和 Skill 定义
│       └── .opencode/
│           ├── agent/           # 7 个 Agent prompt
│           └── skills/          # 26 个 Skill
├── AGENTS.md                   # 系统配置文档
└── README.md                    # 说明文档
```

---

## 安装依赖

```bash
cd ./.ai-team
pip install -r requirements.txt
```

---

## 常见问题

### Q1：如何判断是否使用了 Native Mode？

观察启动时的提示：
- 有 API：显示 Agent 列表和 Workflows
- 无 API：显示配置引导

### Q2：Native Mode 下任务卡住了怎么办？

输入 `/compact` 让 AI 重新对齐上下文。

### Q3：如何切换到有 API 的模式？

编辑 `.ai-team/.env`，填入有效的 API Key，然后重启 OpenCode。

---

## 复制到新环境

```bash
# 1. 复制文件夹
cp -r ./opencode_MCP_SwiftOperate /新项目目录/

# 2. 安装依赖
cd /新项目目录/opencode_MCP_SwiftOperate/.ai-team
pip install -r requirements.txt

# 3. 配置 MCP（如果需要）
mkdir -p ~/.mcp
cp /新项目目录/opencode_MCP_SwiftOperate/opencode.json ~/.mcp/agent-team.json
```