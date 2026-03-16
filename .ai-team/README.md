# LLM Agent Team - 技术文档

## 概述

LLM 驱动的 Agent 开发团队，支持动态模型选择和并行执行。

---

## 目录结构

```
opencode_MCP_SwiftOperate/
├── .ai-team/                      # 核心代码
│   ├── config/
│   │   └── agents.yaml            # Agent 和工作流配置
│   ├── src/
│   │   ├── core/
│   │   │   ├── orchestrator.py    # 调度器
│   │   │   ├── router.py          # LLM 路由
│   │   │   ├── workflow.py        # 工作流
│   │   │   ├── skill_loader.py    # Skill 加载
│   │   │   └── config.py          # 配置加载
│   │   ├── agents/
│   │   │   └── base.py            # Agent 基类
│   │   └── utils/
│   │       └── banner.py          # Logo
│   ├── opencode-agent-skill/
│   │   └── .opencode/
│   │       ├── agent/             # 7 个 Agent prompt
│   │       └── skills/            # 26 个 Skills
│   ├── mcp_server.py              # MCP 服务
│   ├── main.py                    # 入口
│   ├── proof.py                   # 测试
│   └── requirements.txt           # 依赖
├── AGENTS.md                      # 系统配置文档
└── README.md                       # 说明文档
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

### 模式一：有外部 API Key

当你配置了有效的 API Key（如 OpenRouter）时，系统会调用外部 LLM 执行任务。

#### 配置 API Key

```bash
cd ./.ai-team
cp .env.example .env
# 编辑 .env，填入你的 API Key
```

推荐 OpenRouter：
```
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxx
```

#### 使用方式

1. 启动 OpenCode → 输入 `开始`
2. 输入需求，例如：`开发一个 todo app`
3. 系统自动执行，工作流自动流转直到完成

---

### 模式二：无 API Key（Native Mode）

没有配置有效 API Key 时，使用当前 AI 直接执行任务。

#### 特点

- ✅ 无需 API Key
- ✅ 使用当前 AI 能力
- ⚠️ 每个阶段完成后需要确认才能继续
- ⚠️ 复杂任务建议先呼出对应 Agent 角色

#### 使用方式

1. 启动 OpenCode → 输入 `开始`
2. 选择"没有 API Key"

```
【⚙️ API 配置检查】

我检测到你的 .env 还没有配置有效的 API Key。

请选择：
1. 提供 API Key，我帮你配置
2. 回复"没有"，我将使用当前 AI 直接执行任务
```

3. 输入需求，例如：`开发一个 todo app`

#### Native Mode 工作流程示例

```
用户: 开发一个 todo app

AI:
【第一阶段 - Architect】
我理解你的需求：开发一个简单的 Todo 应用。

[暂停等待确认]
用户: 继续

AI:
【第二阶段 - Frontend + Backend】
[开始编写代码]

[暂停等待确认]
用户: 继续

AI:
【第三阶段 - Guardian】
[运行测试，检查代码]

完成！
```

#### ⚠️ 关键提示

1. **每个阶段都需要确认**：看到 "✅ 已完成 xxx，等待确认继续..." 时，输入"继续"

2. **建议先呼出 Agent 角色**：
   - "现在你扮演 frontend-dev agent"
   - "现在你扮演测试工程师"

3. **卡住时**：输入 `/compact` 重新对齐上下文

---

## MCP 工具

### execute_workflow

```python
execute_workflow(task: str, workflow: str) -> dict
```

- `task`: 用户需求描述
- `workflow`: 工作流名称

### continue_workflow

Native Mode 下继续工作流。

```python
continue_workflow(task: str, workflow: str, completed_agents: list) -> dict
```

### execute_agent

调用单个 Agent。

```python
execute_agent(agent: str, task: str) -> dict
```

### list_workflows / list_agents

列出所有工作流 / Agent。

---

## 配置详解

### agents.yaml

```yaml
agents:
  architect:
    model: "google/gemini-3.1-pro-preview"
    temperature: 0.3
    skills:
      - "architecture-design"
      - "prd-methodology"
    
  guardian:
    model: "minimax-m2.5"
    skills:
      - "test-checklist"
      - "security-audit"
      - "code-refactoring"
      - "pytest-guide"
      - "e2e-testing"
      - "integration-testing"
      - "vulnerability-scan"
      - "owasp-security"
      - "bug-bounty"

workflows:
  quick_dev:
    steps:
      - ["architect"]
      - ["frontend-dev", "backend-dev"]
      - ["guardian"]
```

---

## Skills 列表（26个）

### 开发类
- architecture-design, prd-methodology
- dev-standards, code-generation, code-refactoring
- composition-patterns

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

---

## 测试

### 运行测试

```bash
python3 proof.py
```

预期输出：
```
=== LLM Agent System - Proof of Concept ===

✓ Config loading: PASS
✓ Skill loader: PASS (26 skills)
✓ Agent node creation: PASS
✓ Workflow execution: PASS

=== All Tests PASSED ===
```

---

## 故障排除

### MCP 服务未启动

```bash
python3 ./.ai-team/mcp_server.py
```

### 导入错误

```bash
# 检查 Python 路径
python3 -c "import sys; print(sys.path)"

# 手动添加路径
export PYTHONPATH=./ai-team:$PYTHONPATH
```

### API 配置检查

```bash
python3 -c "
from src.core.config_checker import check_api_config
result = check_api_config()
print(result)
"
```

---

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