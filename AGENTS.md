# LLM Agent System - 项目总览

> 真正的 LLM 驱动 Autonomous Agent 系统
> 支持**动态模型选择** - 根据项目复杂度自动选择合适的模型

---

## 🚀 启动

读取本文件后，**首先执行配置检查**：

1. 读取 `.env` 文件检查是否有有效的 API Key
2. 如果没有有效的 API Key，显示配置引导提示

```
                                                                  
  ██████                                        ██      ██    ██  
██        ██████  ████      ██████  ██  ████  ████████  ██    ██  
  ████    ██    ██    ██  ██    ██  ████        ██      ██    ██  
      ██  ██    ██    ██  ██    ██  ██          ██      ██    ██  
██████    ██    ██    ██    ██████  ██            ████    ████    
                                                                  

  🟡 LLM Agent Team  v1.0
  Dynamic Model | Parallel Exec | Auto-Security
```

### ⚙️ 配置检查

**如果检测到有效的 API Key**（如 OpenRouter），直接显示 Agent 列表：

```
【🎯 Orchestrator】
✅ System ready, Agent Team loaded.

Available Agents (7):
  🎯 architect        → 需求分析、任务分发
  🎨 ui-prompt        → UI 提示词工程
  🖼️ ui-generator    → UI 可视化生成
  👨‍💻 frontend-dev   → 前端开发
  🔧 backend-dev     → 后端开发
  🛡️ guardian        → 质量守护 (QA+安全)
  🚀 operator        → DevOps 运维

Workflows:
  full_product     → 完整产品开发
  quick_dev        → 快速开发
  frontend_only    → 只做前端
  backend_only     → 只做后端
  ui_design        → UI 设计
  deployment       → 部署

Dynamic Model Selection: Auto-selects best model based on task complexity.
Describe your requirements, I'll coordinate the appropriate Agent team.
```

**如果检测到没有有效的 API Key**，显示配置引导：

```
【⚙️ API 配置检查】

我检测到你的 .env 还没有配置有效的 API Key。

支持的 API：
- OpenRouter (推荐，支持多种模型)
- OpenAI
- Anthropic
- Google
- Minimax

请选择：
1. 提供 API Key，我帮你配置（例如：sk-or-v1-xxx）
2. 回复"没有"，我将使用当前 AI 直接执行任务

请回复你的选择：
```

> ⚠️ 如果用户选择"没有"，后续所有 Agent 工作由**当前 AI（我）**直接完成，不需要调用外部 LLM。

> ⚠️ 不要询问用户"选择哪个角色" - 根据用户描述自动判断。

---

## ⚠️ 重要：执行任务必须使用 MCP 工具

禁止直接运行 `python3 main.py`。
收到任何开发需求时，自动判断并调用对应 MCP 工具：

- 默认使用 `llm_agents__execute_workflow`，workflow 根据需求自动选择：
  - 完整产品 → `full_product`
  - 快速开发 → `quick_dev`  
  - 只做前端 → `frontend_only`
  - 只做后端 → `backend_only`
  - UI设计 → `ui_design`
  - 部署 → `deployment`

- Native Mode（无 API Key）时：
  - 使用 `execute_workflow` 开始工作流
  - 每个阶段完成后，使用 `continue_workflow` 继续
  - 已完成的 Agent 列表通过参数传递

不需要用户指定工具名或 workflow 名，AI 自行判断后直接调用。



## 架构

```
┌─────────────────────────────────────────────────────────────┐
│                      AutoOrchestrator                       │
│              (LLM-driven ReAct Pattern)                     │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐    ┌──────────┐    ┌──────────┐             │
│  │  Router  │───▶│  Agent   │───▶│  Skill   │             │
│  │  (LLM)   │    │  (LLM)   │    │  Loader  │             │
│  └──────────┘    └──────────┘    └──────────┘             │
└─────────────────────────────────────────────────────────────┘
```

## Agents (7)

| Agent | Model | 职责 |
|-------|-------|------|
| architect | google/gemini-3.1-pro-preview | 需求分解、任务分发 |
| ui-prompt | minimax-m2.5 | UI 提示词工程 |
| ui-generator | openai/gpt-5.4 | UI 可视化生成 |
| frontend-dev | minimax-m2.5 | 前端开发 |
| backend-dev | anthropic/claude-4.6-sonnet | 后端开发 |
| guardian | minimax-m2.5 | 质量守护（QA+安全） |
| operator | google/gemini-3.1-flash-lite-preview | DevOps 运维 |

## Skills (27)

### 开发类
- architecture-design, prd-methodology
- dev-standards, code-generation, code-refactoring
- code-analysis, composition-patterns

### UI 类
- ui-figma-playbook, ui-imagen-guide, ui-aistudio-guide
- web-design-guidelines

### 测试类
- test-checklist, pytest-guide, e2e-testing, integration-testing

### 安全类
- security-audit, vulnerability-scan, owasp-security, bug-bounty

### DevOps 类
- devops-automation, vercel-deploy

### 其他
- mvp-sequencing, protocol-design, token-economics
- changelog-format, blockchain-standards, x-content-strategy

## 工作流

| Workflow | 步骤 |
|----------|------|
| full_product | architect → ui-prompt → ui-generator → frontend-dev → backend-dev → guardian |
| quick_dev | [architect] → [frontend-dev + backend-dev] → [guardian] |
| frontend_only | architect → ui-prompt → frontend-dev → guardian |
| backend_only | architect → backend-dev → guardian |
| deployment | operator → guardian |
| ui_design | architect → ui-prompt → ui-generator |

---

## 开发规范（AI 协议整合）

### 一、技术决策权限

| 决策类型 | 权限归属 |
|----------|----------|
| 技术选型（语言、框架、库） | **自主决定** |
| 代码实现细节 | **自主决定** |
| 新建文件 / 新建模块 | **报备后执行** |
| 架构调整（目录结构、接口设计） | **需确认** |
| 删除已有文件或模块 | **需确认** |
| 引入新的第三方依赖 | **报备后执行** |

### 二、汇报规范

#### 方案汇报格式
```
【我理解的需求】用一句话复述需求的理解
【实现方案】用非技术语言描述怎么做
【预计工作量】大概需要多长时间 / 多少步骤
【需要确认的地方】列出选项和各自的业务影响
```

#### 进度汇报格式
```
【当前进度】做到哪一步了
【遇到的情况】是否有意外（用业务语言描述）
【下一步】接下来要做什么
【是否需要确认】是 / 否
```

#### 完成汇报格式
```
【完成内容】做了什么
【验证结果】怎么证明它是对的
【注意事项】使用时需要知道的事情
```

### 三、执行规范

**动手前必须检查**：
1. 影响哪些已有功能
2. 有没有更简单的实现方式
3. 改完后怎么验证

**完成标准**：代码已运行 + 输出符合预期。禁止未经验证就汇报完成。

### 四、代码规范

- **DRY**：相同逻辑只写一次，不重复
- **KISS**：能简单解决的不过度设计
- 注释用**中文**，变量和函数命名用**英文**
- 禁止硬编码密钥、密码，统一从环境变量读取
- 数据库结构变更必须写 migration

### 五、受保护文件（未经授权禁止修改）

| 文件 / 目录 | 原因 |
|-------------|------|
| `.env` / `.env.*` | 环境配置，改错直接宕机 |
| `**/migrations/**` | 数据库历史记录，不可逆 |
| `**/generated/**` | 自动生成文件，改了会被覆盖 |
| `package-lock.json` / `yarn.lock` | 依赖锁定 |
| `.github/`、`Dockerfile`、`docker-compose.yml` | CI/CD 配置 |

### 六、熔断机制

**情况 A：执行卡住了**
```
停下来，汇报：
1. 卡在哪个功能点
2. 预计影响什么
3. 解决方向是什么
等确认后继续。
```

**情况 B：上下文混乱 / 越改越乱**
```
/compact
重新读取 AGENTS.md
把当前状态重新对齐再继续
```

---

## 快速开始

```bash
cd ./.ai-team
pip install -r requirements.txt
cp .env.example .env

# 列出 agents
python3 main.py --list-agents

# 执行任务
python3 main.py "Build a todo app"

# 切换模型
python3 main.py --switch architect openai/gpt-4
```

## 修改模型

编辑 `llm-agents/config/agents.yaml`:
```yaml
agents:
  architect:
    model: "minimax-m2.5"  # 改成想要的模型
```

---

## 动态模型选择 (D)

系统支持根据项目复杂度自动为每个 Agent 选择合适的模型。

### 使用方式

```bash
# 自动模式（推荐）- 自动分析复杂度并选择模型
python main.py "build a todo app" -w quick_dev --auto

# 手动模式 - 显示复杂度分析和模型选择确认
python main.py "build an ERP system" -w full_product

# 禁用动态选择 - 使用配置文件中的固定模型
python main.py "build a simple page" --no-dynamic
```

### 复杂度级别

| 级别 | 适用场景 | 示例 |
|------|----------|------|
| low | 简单页面 | landing page, 静态页面 |
| medium | 中等复杂度 | 登录系统、CURD |
| high | 复杂系统 | ERP、电商、支付 |
| advanced | 企业级/区块链 | DeFi、SaaS |

### 模型选择规则

| Agent | low | medium | high | advanced |
|-------|-----|--------|------|----------|
| architect | gemini-flash | gemini-pro | claude-sonnet | gpt-5.4 |
| ui-prompt | minimax | minimax | gemini-flash | gemini-pro |
| ui-generator | minimax | gemini-flash | gpt-5.4 | gpt-5.4 |
| frontend-dev | minimax | gemini-flash | gpt-5.4 | gpt-5.4 |
| backend-dev | gemini-flash | claude-sonnet | gpt-5.4 | gpt-5.4 |
| guardian | minimax | minimax | gemini-flash | gemini-pro |
| operator | minimax | minimax | gemini-flash | gemini-flash |

### MCP Server

通过 Claude Code / OpenCode 调用。配置 `~/.mcp/agent-team.json`：

```json
{
  "mcpServers": {
    "agent-team": {
      "command": "python3",
      "args": ["./ai-team/mcp_server.py"]
    }
  }
}
```

---

## 文件结构

```
./.ai-team/
├── config/                      # 配置文件
│   └── agents.yaml              # Agent 和工作流配置
├── src/                        # 源代码
│   ├── core/                   # 核心模块
│   │   ├── orchestrator.py     # 调度器
│   │   ├── complexity_analyzer.py  # 复杂度分析
│   │   ├── dynamic_model_selector.py # 动态模型选择
│   │   ├── router.py           # LLM 路由
│   │   ├── config.py          # 配置加载
│   │   ├── model_factory.py   # 模型工厂
│   │   ├── skill_loader.py    # Skill 加载
│   │   └── workflow.py        # 工作流
│   └── agents/                 # Agent 基类
│       └── base.py
├── opencode-agent-skill/       # Agent 和 Skill 定义
│   └── .opencode/
│       ├── agent/             # 7 个 Agent prompt
│       └── skills/            # 26 个 Skill
├── mcp_server.py              # MCP Server
├── main.py                   # 入口
├── dev.sh                    # 开发脚本
├── install.sh                # 安装脚本
├── proof.py                  # 测试
└── requirements.txt          # Python 依赖
```
## 可用工具

你有一个 MCP 工具 `llm_agents`，包含以下函数：

### 核心工具
- `execute_workflow(task, workflow)` — 执行开发工作流
- `continue_workflow(task, workflow, completed_agents)` — Native Mode 继续工作流
- `execute_agent(agent_name, task, context, history)` — 调用单个 Agent
- `list_workflows()` — 列出所有工作流
- `list_agents()` — 列出所有 Agent

### Native Mode 工作流程

```
1. 用户输入任务
2. 调用 execute_workflow(task, workflow)
3. 返回 stage_complete，等待用户确认
4. 用户说"继续"
5. 调用 continue_workflow(task, workflow, completed_agents)
6. 重复步骤 3-5 直到完成
```

收到开发需求时，**必须调用 MCP 工具**，不要自己直接执行 python 命令。