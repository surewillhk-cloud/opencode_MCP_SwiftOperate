#!/usr/bin/env python3
"""
LLM Agent Team MCP Server
"""

import sys
import json
import asyncio
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from src.core.orchestrator import get_orchestrator
from src.core.config import config
from src.core.complexity_analyzer import ComplexityAnalyzer
from src.core.dynamic_model_selector import DynamicModelSelector


def get_tools():
    return [
        {
            "name": "execute_workflow",
            "description": "执行 Agent 工作流开发项目",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "task": {"type": "string", "description": "任务描述"},
                    "workflow": {
                        "type": "string",
                        "description": "工作流名称: full_product, quick_dev, frontend_only, backend_only, deployment, ui_design",
                    },
                    "auto": {
                        "type": "boolean",
                        "description": "是否自动确认模型选择",
                        "default": True,
                    },
                },
                "required": ["task", "workflow"],
            },
        },
        {
            "name": "execute_agent",
            "description": "直接调用单个 Agent 执行任务（无需完整工作流）",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "agent": {
                        "type": "string",
                        "description": "Agent 名称: architect, ui-prompt, frontend-dev, backend-dev, guardian, operator",
                    },
                    "task": {"type": "string", "description": "任务描述"},
                },
                "required": ["agent", "task"],
            },
        },
        {
            "name": "continue_workflow",
            "description": "继续执行工作流的下一个步骤（native_mode 下使用）",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "last_result": {
                        "type": "string",
                        "description": "上一个步骤的执行结果",
                    },
                    "task": {
                        "type": "string",
                        "description": "原始任务（可选，如果状态丢失需要提供）",
                    },
                    "workflow": {
                        "type": "string",
                        "description": "工作流名称（可选，默认quick_dev）",
                    },
                    "completed_agents": {
                        "type": "array",
                        "description": "已完成的agents列表",
                    },
                },
                "required": ["last_result"],
            },
        },
        {
            "name": "list_workflows",
            "description": "列出所有可用的工作流",
            "inputSchema": {"type": "object", "properties": {}},
        },
        {
            "name": "list_agents",
            "description": "列出所有可用的 Agent",
            "inputSchema": {"type": "object", "properties": {}},
        },
        {
            "name": "analyze_complexity",
            "description": "分析项目复杂度",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "task": {"type": "string", "description": "任务描述"},
                },
                "required": ["task"],
            },
        },
        {
            "name": "select_models",
            "description": "根据复杂度选择模型",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "workflow": {"type": "string"},
                    "task": {"type": "string"},
                },
                "required": ["workflow", "task"],
            },
        },
        {
            "name": "estimate_cost",
            "description": "估算执行成本",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "workflow": {"type": "string"},
                    "task": {"type": "string"},
                },
                "required": ["workflow", "task"],
            },
        },
    ]


_workflow_state = {
    "task": None,
    "workflow_name": None,
    "completed_agents": [],
    "remaining_stages": [],
    "history": [],
}


def handle_tool_call(name: str, arguments: dict) -> str:
    orchestrator = get_orchestrator()

    if name == "execute_workflow":
        task = arguments.get("task", "")
        workflow = arguments.get("workflow", "quick_dev")
        auto = arguments.get("auto", True)
        orchestrator.dynamic_mode = True
        orchestrator.auto_confirm = auto
        result = orchestrator.execute(task, workflow, auto=auto)

        # 保存工作流状态
        _workflow_state["task"] = task
        _workflow_state["workflow_name"] = workflow
        _workflow_state["completed_agents"] = result.get("completed_agents", [])

        return json.dumps(result, ensure_ascii=False, indent=2)

    elif name == "execute_agent":
        from src.agents.base import get_agent_node

        agent_name = arguments.get("agent", "")
        task = arguments.get("task", "")

        if not agent_name:
            return json.dumps({"error": "agent is required"}, ensure_ascii=False)

        try:
            agent = get_agent_node(agent_name)
            result = agent.execute(
                {
                    "task": task,
                    "context": {},
                    "history": [],
                    "iteration": 0,
                }
            )
            return json.dumps(
                {
                    "agent": agent_name,
                    "task": task,
                    "result": result.get("result", ""),
                    "native_mode": result.get("native_mode", False),
                },
                ensure_ascii=False,
                indent=2,
            )
        except Exception as e:
            return json.dumps({"error": str(e)}, ensure_ascii=False)

    elif name == "continue_workflow":
        last_result = arguments.get("last_result", "")

        # 优先使用参数，否则从全局状态获取
        task = arguments.get("task") or _workflow_state.get("task", "")
        workflow_name = arguments.get("workflow") or _workflow_state.get(
            "workflow_name", "quick_dev"
        )
        completed = arguments.get("completed_agents") or _workflow_state.get(
            "completed_agents", []
        )

        if not task:
            return json.dumps(
                {
                    "error": "No active workflow. Please start with execute_workflow first, or provide 'task' parameter."
                },
                ensure_ascii=False,
            )

        # 继续执行
        from src.core.config_checker import has_valid_api_key
        from src.agents.base import get_agent_node
        from src.core.config import config

        is_native = not has_valid_api_key()

        # 获取剩余stages
        steps = config.workflows.get(workflow_name, {}).get("steps", [])

        # 找到当前执行到的位置
        all_stages = [s if isinstance(s, list) else [s] for s in steps]

        # 找到下一个要执行的stage
        next_stage = None
        for stage in all_stages:
            if not all(s in completed for s in stage):
                next_stage = stage
                break

        if not next_stage:
            return json.dumps(
                {"message": "工作流已完成", "completed_agents": completed},
                ensure_ascii=False,
            )

        # 执行下一个stage
        from concurrent.futures import ThreadPoolExecutor, as_completed

        current_task = f"Previous results: {last_result}\n\nOriginal task: {task}"
        context = {"completed": completed}

        if len(next_stage) == 1:
            agent = get_agent_node(next_stage[0])
            result = agent.execute(
                {
                    "task": current_task,
                    "context": context,
                    "history": _workflow_state.get("history", []),
                    "iteration": 0,
                }
            )

            # 更新状态
            _workflow_state["completed_agents"] = completed + next_stage
            _workflow_state["history"] = result.get("history", [])

            if is_native and result.get("native_mode"):
                # 找下一个stage
                remaining = []
                found_current = False
                for stage in all_stages:
                    if stage == next_stage:
                        found_current = True
                    elif found_current:
                        remaining.append(stage)

                return json.dumps(
                    {
                        "result": result.get("result", ""),
                        "completed_agents": completed + next_stage,
                        "next_stage": remaining[0] if remaining else None,
                        "remaining_stages": remaining,
                        "native_mode": True,
                        "waiting_confirmation": len(remaining) > 0,
                        "message": "✅ 工作流已完成！"
                        if not remaining
                        else f"✅ 已完成 {next_stage[0]}，等待确认继续...",
                    },
                    ensure_ascii=False,
                )

            return json.dumps(
                {
                    "result": result.get("result", ""),
                    "completed_agents": completed + next_stage,
                },
                ensure_ascii=False,
            )
        else:
            # 并行执行
            def _run_agent_task(
                agent_name: str, task: str, context: dict, history: list
            ):
                agent = get_agent_node(agent_name)
                return agent.execute(
                    {
                        "task": task,
                        "context": context,
                        "history": history,
                        "iteration": 0,
                    }
                )

            with ThreadPoolExecutor(max_workers=len(next_stage)) as executor:
                futures = {
                    executor.submit(
                        _run_agent_task,
                        agent_name,
                        current_task,
                        context,
                        _workflow_state.get("history", []),
                    ): agent_name
                    for agent_name in next_stage
                }

                stage_results = {}
                for future in as_completed(futures):
                    agent_name = futures[future]
                    try:
                        result = future.result()
                        stage_results[agent_name] = result
                    except Exception as e:
                        stage_results[agent_name] = {"result": f"Error: {e}"}

            combined = "\n\n".join(
                [
                    f"=== {n} ===\n{r.get('result', '')}"
                    for n, r in stage_results.items()
                ]
            )

            _workflow_state["completed_agents"] = completed + next_stage

            # 找下一个stage
            remaining = []
            found_current = False
            for stage in all_stages:
                if stage == next_stage:
                    found_current = True
                elif found_current:
                    remaining.append(stage)

            if is_native:
                return json.dumps(
                    {
                        "result": combined,
                        "completed_agents": completed + next_stage,
                        "next_stage": remaining[0] if remaining else None,
                        "remaining_stages": remaining,
                        "native_mode": True,
                        "waiting_confirmation": len(remaining) > 0,
                        "message": "✅ 工作流已完成！"
                        if not remaining
                        else f"✅ 已完成并行阶段 {next_stage}，等待确认继续...",
                    },
                    ensure_ascii=False,
                )

            return json.dumps(
                {
                    "result": combined,
                    "completed_agents": completed + next_stage,
                },
                ensure_ascii=False,
            )

    elif name == "list_workflows":
        result = {}
        for wf_name, cfg in config.workflows.items():
            steps = cfg.get("steps", [])
            result[wf_name] = " → ".join(steps)
        return json.dumps({"workflows": result}, ensure_ascii=False, indent=2)

    elif name == "list_agents":
        result = {}
        for agent_name, cfg in config.agents.items():
            result[agent_name] = {
                "model": cfg.get("model"),
                "description": cfg.get("description"),
                "skills": cfg.get("skills", []),
            }
        return json.dumps({"agents": result}, ensure_ascii=False, indent=2)

    elif name == "analyze_complexity":
        task = arguments.get("task", "")
        result = ComplexityAnalyzer.analyze(task)
        return json.dumps(result, ensure_ascii=False, indent=2)

    elif name == "select_models":
        workflow = arguments.get("workflow", "quick_dev")
        task = arguments.get("task", "")
        analysis = ComplexityAnalyzer.analyze(task)
        models = DynamicModelSelector.select_models(workflow, analysis)
        return json.dumps(
            {"models": models, "analysis": analysis}, ensure_ascii=False, indent=2
        )

    elif name == "estimate_cost":
        workflow = arguments.get("workflow", "quick_dev")
        task = arguments.get("task", "")
        analysis = ComplexityAnalyzer.analyze(task)
        models = DynamicModelSelector.select_models(workflow, analysis)
        costs = DynamicModelSelector.estimate_cost(models)
        return json.dumps(
            {"costs": costs, "total": costs.get("total", 0)},
            ensure_ascii=False,
            indent=2,
        )

    return json.dumps({"error": f"Unknown tool: {name}"})


def send(obj: dict):
    sys.stdout.write(json.dumps(obj) + "\n")
    sys.stdout.flush()


def main():
    for raw_line in sys.stdin:
        raw_line = raw_line.strip()
        if not raw_line:
            continue

        try:
            request = json.loads(raw_line)
        except json.JSONDecodeError:
            continue

        req_id = request.get("id")
        method = request.get("method", "")

        if method == "initialize":
            send(
                {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "llm-agents", "version": "1.0.0"},
                    },
                }
            )

        elif method == "tools/list":
            send(
                {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"tools": get_tools()},
                }
            )

        elif method == "tools/call":
            params = request.get("params", {})
            tool_name = params.get("name", "")
            arguments = params.get("arguments", {})
            try:
                result_text = handle_tool_call(tool_name, arguments)
                send(
                    {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {"content": [{"type": "text", "text": result_text}]},
                    }
                )
            except Exception as e:
                send(
                    {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {"code": -32000, "message": str(e)},
                    }
                )

        elif method == "notifications/initialized":
            pass  # 不需要回复

        else:
            send(
                {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Method not found: {method}"},
                }
            )


if __name__ == "__main__":
    main()
