from typing import Dict, Any, Optional, List
import logging
from .config import config
from ..agents.base import get_agent_node

logger = logging.getLogger(__name__)

MAX_CONTEXT_LENGTH = 8000


def _truncate_task(task: str, max_length: int = MAX_CONTEXT_LENGTH) -> str:
    """截断过长的任务描述"""
    if len(task) > max_length:
        return task[:max_length] + "\n... (truncated)"
    return task


def execute_workflow(task: str, workflow_name: str) -> Dict[str, Any]:
    """执行预设工作流（legacy 模式）"""

    workflow_cfg = config.workflows.get(workflow_name)
    if not workflow_cfg:
        return {
            "result": f"Workflow '{workflow_name}' not found",
            "history": [],
            "completed_steps": [],
        }

    steps = workflow_cfg.get("steps", [])
    if not steps:
        return {
            "result": f"Workflow '{workflow_name}' has no steps",
            "history": [],
            "completed_steps": [],
        }

    history = []
    current_task = task
    completed_steps = []

    for step in steps:
        logger.info(f"[Workflow] Executing: {step}")

        agent = get_agent_node(step)
        try:
            result = agent.execute(
                {
                    "task": current_task,
                    "context": {"completed": completed_steps},
                    "history": history,
                    "iteration": 0,
                }
            )
        except Exception as e:
            logger.error(f"Workflow step {step} failed: {e}", exc_info=True)
            return {
                "result": f"Error in step {step}: {str(e)}",
                "history": history,
                "completed_steps": completed_steps,
            }

        history.extend(result.get("history", []))
        completed_steps.append(step)

        last_result = result.get("result", "")
        current_task = _truncate_task(
            f"Previous result from {step}: {last_result}\n\nOriginal task: {task}"
        )

    return {
        "result": history[-1].get("content", "") if history else "No result",
        "history": history,
        "completed_steps": completed_steps,
    }


def list_workflows() -> Dict[str, str]:
    """列出所有工作流"""
    workflows = config.workflows
    result = {}
    for name, cfg in workflows.items():
        steps = cfg.get("steps", [])
        formatted = []
        for step in steps:
            if isinstance(step, list):
                formatted.append("[" + " + ".join(step) + "]")
            else:
                formatted.append(step)
        result[name] = " → ".join(formatted)
    return result
