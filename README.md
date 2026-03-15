# ProjectGen — AI 项目策划 SaaS 平台

> 多 Agent 协作驱动的 AI 项目策划平台，自动生成完整的项目描述文档（产品、技术、市场、财务分析）

## 项目复杂度

**级别：Advanced（企业级 SaaS）**

- 7 个 Agent 角色协作
- LangGraph 状态图编排
- 向量知识库（RAG）
- 完整审核流程

## 技术栈

| 层级 | 技术 |
|------|------|
| Agent 框架 | LangGraph v0.2+ |
| LLM 接入 | OpenRouter API |
| 向量数据库 | Qdrant |
| RAG | LlamaIndex |
| 搜索 | Tavily API |
| 后端 | FastAPI |
| 前端 | React + Tailwind CSS |
| 状态持久化 | PostgreSQL |

## 当前进度

### ✅ 已完成

- [x] 项目结构搭建
- [x] 后端依赖配置 (requirements.txt)
- [x] 环境变量模板 (.env.example)
- [x] 模型配置 (config.yaml)
- [x] 配置加载模块 (config.py)
- [x] 数据模型定义 (schemas.py)
- [x] OpenRouter 模型调度层 (models/router.py)
- [x] Agent Prompt 模板库 (agents/prompts.py)
- [x] FastAPI 主应用 (src/main.py)
- [x] 前端项目初始化 (Vite + React + TypeScript)
- [x] Tailwind CSS 集成

### ⏳ 待开发

- [ ] Qdrant 向量知识库服务
- [ ] LangGraph 工作流完整实现（14 个节点）
- [ ] 各 Agent 节点逻辑
- [ ] 审核循环逻辑
- [ ] SSE 实时进度推送
- [ ] 前端页面开发

## 快速开始

### 后端

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入 API Keys

# 运行
python -m src.main
```

### 前端

```bash
cd frontend

npm install
npm run dev
```

## 核心工作流程

```
用户输入想法
    ↓
项目经理需求询问（最多 10 问）
    ↓
需求摘要确认
    ↓
任务拆解 → 并行派发 4 个子 Agent
    ↓
产品/技术/市场/财务 生成章节
    ↓
助理审核（最多 2 次重写）
    ↓
合并总稿
    ↓
项目负责人终审
    ↓
发布 .md 文档（8,000-20,000 字）
```

## MVP 费用上限

| 套餐 | 费用上限 |
|------|----------|
| 免费版 | $0.30 |
| 专业版 | $2.00 |
| 企业版 | $8.00 |

## 文档

- [PRD 完整文档](./ProjectGen_Complete_v3.0%20(3).md)
- [技术架构决策](./ProjectGen_Complete_v3.0%20(3).md#22-框架选型决策langraph-vs-crewai)