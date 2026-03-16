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
│   │   │   ├── config.py          # 配置加载
│   │   │   ├── model_factory.py   # 模型工厂
│   │   │   └── ...                # 其他模块
│   │   ├── agents/
│   │   │   └── base.py            # Agent 基类
│   │   └── utils/
│   │       └── banner.py          # Logo
│   ├── opencode-agent-skill/
│   │   └── .opencode/
│   │       ├── agent/             # 7 个 Agent 定义
│   │       └── skills/            # 26 个 Skills
│   ├── mcp_server.py              # MCP 服务
│   ├── main.py                    # 入口
│   ├── proof.py                   # 测试
│   └── requirements.txt           # 依赖
├── AGENTS.md                      # 系统配置文档
└── README.md                       # 说明文档
```

---

## Agents 详解（7个）

### 1. Architect（架构师）
- **职责**：需求分析、任务分发、进度管理、并发调研
- **可调用子 Agent**：ui-prompt, ui-generator, frontend-dev, backend-dev, guardian, operator
- **Skills**：architecture-design, prd-methodology

### 2. UI-Prompt（UI 提示词工程师）
- **职责**：生成高质量 UI 设计提示词
- **Skills**：ui-figma-playbook, ui-imagen-guide, ui-aistudio-guide

### 3. UI-Generator（UI 可视化生成专家）
- **职责**：根据提示词生成 UI 设计
- **Skills**：ui-figma-playbook, web-design-guidelines

### 4. Frontend-Dev（前端开发者）
- **职责**：前端代码开发
- **Skills**：dev-standards, web-design-guidelines, composition-patterns, vercel-deploy

### 5. Backend-Dev（后端开发者）
- **职责**：后端代码开发
- **Skills**：dev-standards, architecture-design

### 6. Guardian（质量守护者）
- **职责**：QA 测试 + 安全审计
- **Skills**（9个）：test-checklist, pytest-guide, e2e-testing, integration-testing, security-audit, vulnerability-scan, owasp-security, bug-bounty, code-refactoring

### 7. Operator（运维工程师）
- **职责**：部署和运维
- **Skills**：devops-automation, vercel-deploy

---

## Skills 列表（27个）

### 开发类（7个）
- architecture-design - 系统架构设计
- prd-methodology - 需求分析方法
- dev-standards - 开发规范
- code-generation - 代码生成
- code-refactoring - 代码重构
- code-analysis - 代码分析、探索、审计
- composition-patterns - 组件组合模式

### UI 类（4个）
- ui-figma-playbook - Figma 指南
- ui-imagen-guide - Imagen 指南
- ui-aistudio-guide - AISTudio 指南
- web-design-guidelines - 网页设计规范

### 测试类（4个）
- test-checklist - 测试清单
- pytest-guide - Pytest 指南
- e2e-testing - 端到端测试
- integration-testing - 集成测试

### 安全类（4个）
- security-audit - 安全审计
- vulnerability-scan - 漏洞扫描
- owasp-security - OWASP 安全
- bug-bounty - 渗透测试

### DevOps 类（2个）
- devops-automation - DevOps 自动化
- vercel-deploy - Vercel 部署

### 其他类（6个）
- mvp-sequencing - MVP 排序
- protocol-design - 协议设计
- token-economics - 代币经济
- changelog-format - 变更日志
- blockchain-standards - 区块链标准
- x-content-strategy - 内容策略

---

## 工作流详解（7个）

### full_product（完整产品开发）
```
architect → ui-prompt → ui-generator → frontend-dev → backend-dev → guardian
```

### quick_dev（快速开发）⭐推荐
```
[architect] → [frontend-dev + backend-dev] → [guardian]
```

### frontend_only（仅前端）
```
architect → ui-prompt → frontend-dev → guardian
```

### backend_only（仅后端）
```
architect → backend-dev → guardian
```

### frontend_parallel（前端并行）
```
[architect] → [ui-prompt + ui-generator] → [frontend-dev] → [guardian]
```

### deployment（部署）
```
operator → guardian
```

### ui_design（UI 设计）
```
architect → ui-prompt → ui-generator
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

=== All Tests PASSED ===
```

---

## MCP 工具

### execute_workflow(task, workflow)
执行完整工作流

### continue_workflow(task, workflow, completed_agents)
Native Mode 下继续工作流

### execute_agent(agent, task)
调用单个 Agent

### list_workflows
列出所有工作流

### list_agents
列出所有 Agent

---

## Native Mode 实现

### 无 API Key 时的行为

1. Agent 执行时返回 Agent 定义给当前 AI
2. 当前 AI 直接代入角色执行任务
3. 每个阶段完成后暂停，等待确认

### 代码示例

```python
# base.py
def _execute_native(self, task: str) -> dict:
    return {
        "status": "native",
        "agent_name": self.agent_name,
        "agent_definition": self.get_agent_definition(),
        "skills": self.skills,
        "task": task
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

## 测试

### 运行测试

```bash
python3 proof.py
```

---

## 故障排除

### MCP 服务未启动

```bash
python3 ./.ai-team/mcp_server.py
```

### 导入错误

```bash
export PYTHONPATH=./ai-team:$PYTHONPATH
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