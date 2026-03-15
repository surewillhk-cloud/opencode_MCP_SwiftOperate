from typing import Dict, Any, Optional, List
import logging

from .complexity_analyzer import ComplexityLevel

logger = logging.getLogger(__name__)

MODEL_COSTS = {
    "google/gemini-3.1-flash-lite-preview": 0.002,
    "google/gemini-3.1-pro-preview": 0.10,
    "anthropic/claude-4.6-sonnet": 0.15,
    "openai/gpt-5.4": 0.50,
}

MODEL_NAMES = {
    "google/gemini-3.1-flash-lite-preview": "Gemini Flash Lite",
    "google/gemini-3.1-pro-preview": "Gemini Pro",
    "anthropic/claude-4.6-sonnet": "Claude Sonnet",
    "openai/gpt-5.4": "GPT-5.4",
}


class DynamicModelSelector:
    """动态模型选择器 - 根据复杂度为每个 agent 选择模型"""

    MODEL_MAPPING = {
        "architect": {
            ComplexityLevel.LOW: "google/gemini-3.1-flash-lite-preview",
            ComplexityLevel.MEDIUM: "google/gemini-3.1-pro-preview",
            ComplexityLevel.HIGH: "anthropic/claude-4.6-sonnet",
            ComplexityLevel.ADVANCED: "openai/gpt-5.4",
        },
        "ui-prompt": {
            ComplexityLevel.LOW: "google/gemini-3.1-flash-lite-preview",
            ComplexityLevel.MEDIUM: "google/gemini-3.1-flash-lite-preview",
            ComplexityLevel.HIGH: "google/gemini-3.1-pro-preview",
            ComplexityLevel.ADVANCED: "google/gemini-3.1-pro-preview",
        },
        "ui-generator": {
            ComplexityLevel.LOW: "google/gemini-3.1-flash-lite-preview",
            ComplexityLevel.MEDIUM: "google/gemini-3.1-flash-lite-preview",
            ComplexityLevel.HIGH: "openai/gpt-5.4",
            ComplexityLevel.ADVANCED: "openai/gpt-5.4",
        },
        "frontend-dev": {
            ComplexityLevel.LOW: "google/gemini-3.1-flash-lite-preview",
            ComplexityLevel.MEDIUM: "google/gemini-3.1-flash-lite-preview",
            ComplexityLevel.HIGH: "openai/gpt-5.4",
            ComplexityLevel.ADVANCED: "openai/gpt-5.4",
        },
        "backend-dev": {
            ComplexityLevel.LOW: "google/gemini-3.1-flash-lite-preview",
            ComplexityLevel.MEDIUM: "anthropic/claude-4.6-sonnet",
            ComplexityLevel.HIGH: "openai/gpt-5.4",
            ComplexityLevel.ADVANCED: "openai/gpt-5.4",
        },
        "guardian": {
            ComplexityLevel.LOW: "google/gemini-3.1-flash-lite-preview",
            ComplexityLevel.MEDIUM: "google/gemini-3.1-flash-lite-preview",
            ComplexityLevel.HIGH: "google/gemini-3.1-pro-preview",
            ComplexityLevel.ADVANCED: "anthropic/claude-4.6-sonnet",
        },
        "operator": {
            ComplexityLevel.LOW: "google/gemini-3.1-flash-lite-preview",
            ComplexityLevel.MEDIUM: "google/gemini-3.1-flash-lite-preview",
            ComplexityLevel.HIGH: "google/gemini-3.1-pro-preview",
            ComplexityLevel.ADVANCED: "google/gemini-3.1-pro-preview",
        },
    }

    WORKFLOW_AGENTS = {
        "full_product": [
            "architect",
            "ui-prompt",
            "ui-generator",
            "frontend-dev",
            "backend-dev",
            "guardian",
        ],
        "quick_dev": ["architect", "frontend-dev", "backend-dev", "guardian"],
        "frontend_only": ["architect", "ui-prompt", "frontend-dev", "guardian"],
        "backend_only": ["architect", "backend-dev", "guardian"],
        "deployment": ["operator", "guardian"],
        "ui_design": ["architect", "ui-prompt", "ui-generator"],
    }

    @classmethod
    def select_models(
        cls, workflow_name: str, complexity_analysis: Dict[str, Any]
    ) -> Dict[str, str]:
        """根据复杂度为工作流中的每个 agent 选择模型"""
        agents = cls.WORKFLOW_AGENTS.get(workflow_name, [])
        model_selections = {}

        frontend_level = complexity_analysis.get("frontend", {}).get(
            "level", ComplexityLevel.MEDIUM
        )
        backend_level = complexity_analysis.get("backend", {}).get(
            "level", ComplexityLevel.MEDIUM
        )
        ui_level = complexity_analysis.get("ui", {}).get(
            "level", ComplexityLevel.MEDIUM
        )
        overall_level = complexity_analysis.get("overall_level", ComplexityLevel.MEDIUM)

        for agent in agents:
            if agent in ["ui-prompt", "ui-generator"]:
                level = ui_level
            elif agent in ["frontend-dev"]:
                level = frontend_level
            elif agent in ["backend-dev"]:
                level = backend_level
            else:
                level = overall_level

            model = cls.MODEL_MAPPING.get(agent, {}).get(level, "minimax-m2.5")
            model_selections[agent] = model

        return model_selections

    @classmethod
    def estimate_cost(
        cls, model_selections: Dict[str, str], tokens_per_agent: int = 5000
    ) -> Dict[str, float]:
        """估算成本"""
        costs = {}
        for agent, model in model_selections.items():
            cost_per_1k = MODEL_COSTS.get(model, 0.01)
            cost = (tokens_per_agent / 1000) * cost_per_1k
            costs[agent] = cost

        costs["total"] = sum(costs.values())
        return costs

    @classmethod
    def format_selection_report(
        cls,
        workflow_name: str,
        model_selections: Dict[str, str],
        complexity_analysis: Dict[str, Any],
        costs: Dict[str, float],
    ) -> str:
        """格式化选择报告"""
        from .complexity_analyzer import ComplexityAnalyzer

        complexity_desc = ComplexityAnalyzer.get_complexity_description(
            complexity_analysis
        )

        lines = [
            "=== 项目复杂度分析 ===",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            f"📊 整体评估: {complexity_desc}复杂度",
            "",
        ]

        frontend = complexity_analysis.get("frontend", {})
        backend = complexity_analysis.get("backend", {})
        ui = complexity_analysis.get("ui", {})

        if frontend.get("details"):
            lines.append(f"前端 ({', '.join(frontend['details'][:3])}):")

        for agent in ["ui-prompt", "ui-generator", "frontend-dev"]:
            if agent in model_selections:
                model = model_selections[agent]
                cost = costs.get(agent, 0)
                model_name = MODEL_NAMES.get(model, model)
                lines.append(f"  → {agent}: {model_name} (${cost:.3f})")

        if backend.get("details"):
            lines.append(f"后端 ({', '.join(backend['details'][:3])}):")

        for agent in ["backend-dev"]:
            if agent in model_selections:
                model = model_selections[agent]
                cost = costs.get(agent, 0)
                model_name = MODEL_NAMES.get(model, model)
                lines.append(f"  → {agent}: {model_name} (${cost:.3f})")

        lines.extend(
            [
                "",
                "其他:",
            ]
        )

        for agent in ["architect", "guardian", "operator"]:
            if agent in model_selections:
                model = model_selections[agent]
                cost = costs.get(agent, 0)
                model_name = MODEL_NAMES.get(model, model)
                lines.append(f"  → {agent}: {model_name} (${cost:.3f})")

        total = costs.get("total", 0)
        lines.extend(
            [
                "",
                f"💰 预估总成本: ${total:.2f}",
                "",
                "是否确认? [Y/n/a(调整)]: ",
            ]
        )

        return "\n".join(lines)

    @classmethod
    def adjust_models(
        cls, model_selections: Dict[str, str], adjustment: str
    ) -> Dict[str, str]:
        """调整模型选择"""
        new_selections = model_selections.copy()

        level_map = {
            "low": ComplexityLevel.LOW,
            "medium": ComplexityLevel.MEDIUM,
            "high": ComplexityLevel.HIGH,
            "advanced": ComplexityLevel.ADVANCED,
        }

        adjustment_level = level_map.get(adjustment.lower(), ComplexityLevel.MEDIUM)

        for agent in new_selections:
            if agent in cls.MODEL_MAPPING:
                new_selections[agent] = cls.MODEL_MAPPING[agent].get(
                    adjustment_level, new_selections[agent]
                )

        return new_selections
