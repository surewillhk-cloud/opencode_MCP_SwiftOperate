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

#### ⚠️ 关键提示

1. **每个阶段都需要确认**：看到 "✅ 已完成 xxx，等待确认继续..." 时，输入"继续"

2. **建议先呼出 Agent 角色**：
   - "现在你扮演 frontend-dev agent，帮我写一个登录页面"
   - "现在你扮演测试工程师，帮我验证这段代码"

3. **卡住时**：输入 `/compact` 重新对齐上下文

---

## Agents 详解（7个）

### 1. Architect（架构师）⭐⭐⭐⭐⭐

**职责**：需求分析、任务分发、进度管理、并发调研

**使用场景**：
- 用户提出需求，需要任务规划
- 需要技术选型和架构设计
- 需要协调多个 Agent 合作

**可以调用的子 Agent**：
- `ui-prompt` - UI 提示词工程
- `ui-generator` - UI 可视化生成
- `frontend-dev` - 前端开发
- `backend-dev` - 后端开发
- `guardian` - 测试和安全
- `operator` - 部署运维

**加载的 Skills**：
- `architecture-design` - 系统架构设计
- `prd-methodology` - 需求分析方法

**工作方式**：
1. 首先理解用户真正想要什么
2. 并发调研：同时搜索 Web/GitHub/文档
3. 决定哪些 Agent 应该做什么
4. 收集结果并呈现给用户

---

### 2. UI-Prompt（UI 提示词工程师）

**职责**：生成高质量的 UI 设计提示词

**使用场景**：
- 需要为 Figma/Imagen/AISTudio 生成提示词
- 需要设计 prompt 给 ui-generator

**加载的 Skills**：
- `ui-figma-playbook` - Figma 设计指南
- `ui-imagen-guide` - Imagen 使用指南
- `ui-aistudio-guide` - AISTudio 使用指南

**输出**：高质量的 AI 图像生成提示词

---

### 3. UI-Generator（UI 可视化生成专家）

**职责**：根据提示词生成 UI 设计

**使用场景**：
- 需要生成 UI 图像
- 需要可视化设计稿

**加载的 Skills**：
- `ui-figma-playbook` - Figma 设计指南
- `web-design-guidelines` - 网页设计规范

**输出**：UI 设计图像或设计稿

---

### 4. Frontend-Dev（前端开发者）

**职责**：前端代码开发

**使用场景**：
- 需要编写 HTML/CSS/JavaScript
- 需要 React/Vue/Angular 开发
- 需要实现 UI 组件

**加载的 Skills**：
- `dev-standards` - 开发规范
- `web-design-guidelines` - 网页设计规范
- `composition-patterns` - 组件组合模式
- `vercel-deploy` - Vercel 部署

**输出**：可运行的前端代码

---

### 5. Backend-Dev（后端开发者）

**职责**：后端代码开发

**使用场景**：
- 需要 API 开发
- 需要数据库设计
- 需要业务逻辑实现

**加载的 Skills**：
- `dev-standards` - 开发规范
- `architecture-design` - 架构设计

**输出**：可运行的后端代码

---

### 6. Guardian（质量守护者）⭐⭐⭐⭐⭐

**职责**：QA 测试 + 安全审计

**使用场景**：
- 需要测试代码
- 需要安全审计
- 需要代码审查
- 需要漏洞扫描

**加载的 Skills**（共9个）：
- `test-checklist` - 测试清单
- `pytest-guide` - Pytest 指南
- `e2e-testing` - 端到端测试
- `integration-testing` - 集成测试
- `security-audit` - 安全审计
- `vulnerability-scan` - 漏洞扫描
- `owasp-security` - OWASP 安全
- `bug-bounty` - 渗透测试
- `code-refactoring` - 代码重构

**输出**：测试报告、安全报告、代码改进建议

---

### 7. Operator（运维工程师）

**职责**：部署和运维

**使用场景**：
- 需要部署应用到 Vercel
- 需要 CI/CD 配置
- 需要环境配置

**加载的 Skills**：
- `devops-automation` - DevOps 自动化
- `vercel-deploy` - Vercel 部署

**输出**：部署链接、运维配置

---

## Skills 详解（27个）

### 开发类（7个）

| Skill | 作用 | 使用场景 |
|-------|------|----------|
| `architecture-design` | 系统架构设计、技术选型、创建 ADR | 设计新系统、选择数据库、做技术决策 |
| `prd-methodology` | 需求分析方法、PRD 撰写 | 分析需求、撰写产品文档 |
| `dev-standards` | 代码规范、最佳实践 | 编写符合规范的代码 |
| `code-generation` | 代码生成模板 | 快速生成重复代码 |
| `code-refactoring` | 代码重构方法、模式 | 重构烂代码、提升质量 |
| `code-analysis` | 代码分析、探索、审计 | 理解代码库、审计代码、提出优化方案 |
| `composition-patterns` | 组件组合模式 | React/Vue 组件设计 |

### UI 类（4个）

| Skill | 作用 | 使用场景 |
|-------|------|----------|
| `ui-figma-playbook` | Figma 使用指南、设计流程 | Figma 设计 |
| `ui-imagen-guide` | Google Imagen 使用指南 | AI 图像生成 |
| `ui-aistudio-guide` | AI Studio 使用指南 | AI 图像生成 |
| `web-design-guidelines` | 网页设计规范、响应式布局 | 网页设计 |

### 测试类（4个）

| Skill | 作用 | 使用场景 |
|-------|------|----------|
| `test-checklist` | 测试清单、测试策略 | 规划测试 |
| `pytest-guide` | Pytest 使用指南 | Python 单元测试 |
| `e2e-testing` | 端到端测试方法 | 用户流程测试 |
| `integration-testing` | 集成测试方法 | 模块集成测试 |

### 安全类（4个）

| Skill | 作用 | 使用场景 |
|-------|------|----------|
| `security-audit` | 安全审计方法 | 代码安全审查 |
| `vulnerability-scan` | 漏洞扫描方法 | 发现安全漏洞 |
| `owasp-security` | OWASP Top 10 | Web 安全 |
| `bug-bounty` | 渗透测试方法 | 安全测试 |

### DevOps 类（2个）

| Skill | 作用 | 使用场景 |
|-------|------|----------|
| `devops-automation` | CI/CD 自动化配置 | 自动化部署 |
| `vercel-deploy` | Vercel 部署指南 | Vercel 托管部署 |

### 其他类（6个）

| Skill | 作用 | 使用场景 |
|-------|------|----------|
| `mvp-sequencing` | MVP 排序方法 | 产品规划 |
| `protocol-design` | 协议设计方法 | API 设计 |
| `token-economics` | 代币经济模型 | Web3 项目 |
| `changelog-format` | 变更日志格式 | 版本发布 |
| `blockchain-standards` | 区块链标准 | 区块链开发 |
| `x-content-strategy` | 内容策略 | 内容运营 |

---

## 工作流详解（7个）

### 1. full_product（完整产品开发）

```
步骤：architect → ui-prompt → ui-generator → frontend-dev → backend-dev → guardian
```

**详细流程**：
1. **Architect**：分析需求、技术选型、任务分发
2. **UI-Prompt**：生成 UI 设计提示词
3. **UI-Generator**：生成 UI 设计图像
4. **Frontend-Dev**：开发前端代码
5. **Backend-Dev**：开发后端代码
6. **Guardian**：测试 + 安全审计

**适用场景**：全新产品、从零开始的项目

---

### 2. quick_dev（快速开发）⭐⭐⭐⭐⭐

```
步骤：[architect] → [frontend-dev + backend-dev] → [guardian]
```

**详细流程**：
1. **Architect**：分析需求，分发任务
2. **Frontend-Dev + Backend-Dev**：并行开发
3. **Guardian**：测试 + 安全审计

**特点**：并行执行，节省时间

**适用场景**：快速原型、小型项目

---

### 3. frontend_only（仅前端）

```
步骤：architect → ui-prompt → frontend-dev → guardian
```

**详细流程**：
1. **Architect**：需求分析
2. **UI-Prompt**：UI 提示词
3. **Frontend-Dev**：前端开发
4. **Guardian**：测试

**适用场景**：纯前端项目、静态网站

---

### 4. backend_only（仅后端）

```
步骤：architect → backend-dev → guardian
```

**详细流程**：
1. **Architect**：需求分析
2. **Backend-Dev**：后端开发
3. **Guardian**：测试 + 安全

**适用场景**：API 服务、后端系统

---

### 5. frontend_parallel（前端并行）

```
步骤：[architect] → [ui-prompt + ui-generator] → [frontend-dev] → [guardian]
```

**详细流程**：
1. **Architect**：需求分析
2. **UI-Prompt + UI-Generator**：并行生成 UI 提示词和设计
3. **Frontend-Dev**：前端开发
4. **Guardian**：测试

**适用场景**：需要 UI 设计和前端同时进行

---

### 6. deployment（部署）

```
步骤：operator → guardian
```

**详细流程**：
1. **Operator**：部署应用
2. **Guardian**：验证部署、检查安全

**适用场景**：已开发完成，需要部署

---

### 7. ui_design（UI 设计）

```
步骤：architect → ui-prompt → ui-generator
```

**详细流程**：
1. **Architect**：需求分析
2. **UI-Prompt**：生成提示词
3. **UI-Generator**：生成 UI 设计

**适用场景**：只需要设计稿，不需要代码

---

## MCP 工具详解

### execute_workflow

执行完整工作流。

```python
# 参数
task: str          # 用户需求描述
workflow: str      # 工作流名称 (full_product, quick_dev, etc.)
auto: bool         # 是否自动确认模型选择

# 示例
execute_workflow(task="开发一个 todo app", workflow="quick_dev")
```

---

### continue_workflow

Native Mode 下继续工作流。

```python
# 参数
task: str              # 原始任务描述
workflow: str          # 工作流名称
completed_agents: list # 已完成的 Agent 列表
last_result: str       # 上一个步骤的执行结果

# 示例
continue_workflow(task="开发一个 todo app", workflow="quick_dev", completed_agents=["architect"])
```

---

### execute_agent

调用单个 Agent。

```python
# 参数
agent: str    # Agent 名称 (architect, frontend-dev, etc.)
task: str     # 任务描述

# 示例
execute_agent(agent="frontend-dev", task="实现登录页面")
```

---

### list_workflows

列出所有可用工作流。

### list_agents

列出所有可用 Agent。

### analyze_complexity

分析项目复杂度。

### select_models

根据复杂度选择模型。

### estimate_cost

估算执行成本。

---

## MCP 配置

如果 OpenCode 没有自动加载 MCP，手动配置：

```bash
mkdir -p ~/.mcp
cp ./opencode_MCP_SwiftOperate/opencode.json ~/.mcp/agent-team.json
```

或者手动创建 `~/.mcp/agent-team.json`：

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

## 目录结构

```
opencode_MCP_SwiftOperate/
├── .ai-team/                   # 核心代码
│   ├── config/
│   │   └── agents.yaml         # Agent 和工作流配置
│   ├── src/
│   │   ├── core/               # 核心模块
│   │   │   ├── orchestrator.py # 调度器
│   │   │   ├── router.py       # LLM 路由
│   │   │   ├── workflow.py     # 工作流
│   │   │   ├── config.py       # 配置加载
│   │   │   ├── model_factory.py# 模型工厂
│   │   │   ├── skill_loader.py # Skill 加载
│   │   │   └── ...            # 其他模块
│   │   └── agents/
│   │       └── base.py         # Agent 基类
│   ├── opencode-agent-skill/
│   │   └── .opencode/
│   │       ├── agent/           # 7 个 Agent 定义
│   │       │   ├── architect.md
│   │       │   ├── frontend-dev.md
│   │       │   ├── backend-dev.md
│   │       │   ├── guardian.md
│   │       │   ├── ui-prompt.md
│   │       │   ├── ui-generator.md
│   │       │   └── operator.md
│   │       └── skills/          # 26 个 Skill
│   │           ├── architecture-design/
│   │           ├── pytest-guide/
│   │           ├── security-audit/
│   │           └── ... (共 26 个)
│   ├── mcp_server.py            # MCP 服务入口
│   ├── main.py                  # CLI 入口
│   ├── proof.py                 # 测试
│   └── requirements.txt         # Python 依赖
├── AGENTS.md                    # AI Agent 系统配置
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

### Q4：Guardian 有 9 个 Skills，具体用哪些？

根据任务自动选择：
- 测试任务 → test-checklist, pytest-guide
- 安全任务 → security-audit, vulnerability-scan
- 重构任务 → code-refactoring

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