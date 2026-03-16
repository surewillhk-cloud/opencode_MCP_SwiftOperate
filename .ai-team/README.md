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

## 快速开始

### 1. 安装依赖

```bash
cd ./.ai-team
pip install -r requirements.txt
```

### 2. 配置 MCP

创建 `~/.mcp/agent-team.json`：

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

### 3. 验证

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
✓ Orchestrator: PASS

=== All Tests PASSED ===
```

---

## MCP 工具

### execute_workflow

```python
execute_workflow(task: str, workflow: str) -> dict
```

**参数：**
- `task`: 用户需求描述
- `workflow`: 工作流名称

**返回值：**
```python
{
  "status": "success" | "native_mode" | "error",
  "message": "...",
  "results": {...}
}
```

### continue_workflow

Native Mode 下继续工作流。

```python
continue_workflow(task: str, workflow: str, completed_agents: list) -> dict
```

**参数：**
- `task`: 原始任务描述
- `workflow`: 工作流名称
- `completed_agents`: 已完成的 Agent 列表

### execute_agent

调用单个 Agent。

```python
execute_agent(agent_name: str, task: str, context: dict, history: list) -> dict
```

**参数：**
- `agent_name`: Agent 名称
- `task`: 任务描述
- `context`: 上下文
- `history`: 历史记录

### list_workflows

列出所有工作流。

### list_agents

列出所有 Agent。

---

## Native Mode 实现

### base.py

```python
def _execute_native(self, task: str) -> dict:
    """
    Native Mode: 返回 Agent 定义给当前 AI
    """
    return {
        "status": "native",
        "agent_name": self.agent_name,
        "agent_definition": self.get_agent_definition(),
        "skills": self.skills,
        "task": task
    }
```

### orchestrator.py

```python
# 检测 native mode
if is_native_mode():
    # 返回阶段结果，暂停工作流
    return {
        "status": "stage_complete",
        "completed_agents": completed,
        "next_agents": next_agents,
        "message": "等待继续..."
    }
```

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
- architecture-design
- prd-methodology
- dev-standards
- code-generation
- code-refactoring
- composition-patterns

### UI 类
- ui-figma-playbook
- ui-imagen-guide
- ui-aistudio-guide
- web-design-guidelines

### 测试类
- test-checklist
- pytest-guide
- e2e-testing
- integration-testing

### 安全类
- security-audit
- vulnerability-scan
- owasp-security
- bug-bounty

### DevOps 类
- devops-automation
- vercel-deploy

### 其他
- mvp-sequencing
- protocol-design
- token-economics
- changelog-format
- blockchain-standards
- x-content-strategy

---

## 测试

### 运行测试

```bash
python3 proof.py
```

### 测试新 Skills

```bash
python3 -c "
from src.core.skill_loader import SkillLoader

skills = ['pytest-guide', 'e2e-testing', 'vulnerability-scan', 'owasp-security', 'bug-bounty']
for s in skills:
    content = SkillLoader.load_skill(s)
    print(f'{s}: {len(content)} chars')
"
```

### 测试 Guardian 配置

```bash
python3 -c "
from src.agents.base import get_agent_node

guardian = get_agent_node('guardian')
print('Guardian skills:', guardian.skills)
"
```

---

## 故障排除

### MCP 服务未启动

```bash
# 手动测试
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
 |____/|_| |_| |_|\__,_|_|   \__|  \___/  
 
  🟡 LLM Agent Team  v1.0
  Dynamic Model | Parallel Exec | Auto-Security
```
