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


def handle_tool_call(name: str, arguments: dict) -> str:
    orchestrator = get_orchestrator()

    if name == "execute_workflow":
        task = arguments.get("task", "")
        workflow = arguments.get("workflow", "quick_dev")
        auto = arguments.get("auto", True)
        orchestrator.dynamic_mode = True
        orchestrator.auto_confirm = auto
        result = orchestrator.execute(task, workflow, auto=auto)
        return json.dumps(result, ensure_ascii=False, indent=2)

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
        return json.dumps({"models": models, "analysis": analysis}, ensure_ascii=False, indent=2)

    elif name == "estimate_cost":
        workflow = arguments.get("workflow", "quick_dev")
        task = arguments.get("task", "")
        analysis = ComplexityAnalyzer.analyze(task)
        models = DynamicModelSelector.select_models(workflow, analysis)
        costs = DynamicModelSelector.estimate_cost(models)
        return json.dumps({"costs": costs, "total": costs.get("total", 0)}, ensure_ascii=False, indent=2)

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
            send({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "llm-agents", "version": "1.0.0"},
                },
            })

        elif method == "tools/list":
            send({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"tools": get_tools()},
            })

        elif method == "tools/call":
            params = request.get("params", {})
            tool_name = params.get("name", "")
            arguments = params.get("arguments", {})
            try:
                result_text = handle_tool_call(tool_name, arguments)
                send({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": result_text}]
                    },
                })
            except Exception as e:
                send({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32000, "message": str(e)},
                })

        elif method == "notifications/initialized":
            pass  # 不需要回复

        else:
            send({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"},
            })


if __name__ == "__main__":
    main()