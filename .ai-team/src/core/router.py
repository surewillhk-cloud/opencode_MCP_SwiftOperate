from typing import Dict, Any, List, Optional
import logging
from langchain_core.messages import HumanMessage, SystemMessage

from .config import config
from .model_factory import ModelFactory

logger = logging.getLogger(__name__)


class LLMRouter:
    """LLM 驱动的路由器 - 让 LLM 决定使用哪个 Agent"""

    def __init__(self):
        router_model = config.defaults.get(
            "router_model", "nvidia/nemotron-3-super:free"
        )
        self.llm = ModelFactory.get_model(router_model)
        self.max_history_length = 5

    @staticmethod
    def _extract_response_content(response: Any) -> str:
        """安全提取响应内容"""
        if hasattr(response, "content"):
            content = response.content
            if isinstance(content, str):
                return content
            elif isinstance(content, list):
                return " ".join(str(item) for item in content)
        return str(response) if response else ""

    @staticmethod
    def _extract_agent_name(
        response_text: str, available_agents: List[str]
    ) -> Optional[str]:
        """从响应中提取 agent 名称"""
        response_lower = response_text.lower()

        for agent_name in available_agents:
            if agent_name.lower() in response_lower:
                return agent_name

        return None

    def route(
        self, task: str, available_agents: List[str], context: Dict = None
    ) -> str:
        """让 LLM 决定使用哪个 Agent"""

        agent_descriptions = []
        for agent_name in available_agents:
            cfg = config.get_agent_config(agent_name)
            agent_descriptions.append(
                f"- {agent_name}: {cfg.get('description', 'No description')}"
            )

        context_str = ""
        if context:
            context_str = f"\n\nContext:\n" + "\n".join(
                [f"{k}: {v}" for k, v in context.items()]
            )

        prompt = f"""You are a router. Analyze the task and select the best agent.

Task: {task}
{context_str}

Available agents:
{chr(10).join(agent_descriptions)}

Based on the task, which agent should handle this? 
Consider:
1. What type of work is needed?
2. Which agent has the right skills?
3. What's the logical order?

Return ONLY the agent name (e.g., "frontend-dev"). Nothing else."""

        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            result_text = self._extract_response_content(response)

            for agent_name in available_agents:
                if agent_name.lower() in result_text.lower():
                    return agent_name

            logger.warning(
                f"Router: no valid agent matched, defaulting to {available_agents[0]}"
            )
            return available_agents[0]
        except Exception as e:
            logger.error(f"Router error: {e}", exc_info=True)
            return available_agents[0] if available_agents else None

    def should_continue(self, task: str, result: str, history: List[Dict]) -> bool:
        """让 LLM 判断是否继续执行"""

        prompt = f"""Analyze if the task is complete.

Original Task: {task}

Last Result:
{result}

History:
{chr(10).join([f"- {h.get('role')}: {h.get('content', '')[:100]}" for h in history[-5:]])}

Is the task complete? Consider:
1. Has the main request been fulfilled?
2. Are there remaining sub-tasks?
3. Does the result look final or partial?

Return ONLY "yes" if more work is needed, or "no" if the task is complete."""

        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            result_text = self._extract_response_content(response)
            result_clean = result_text.strip().lower()
            return "yes" in result_clean and "no" not in result_clean
        except Exception as e:
            logger.warning(f"Router should_continue error: {e}")
            return False

    def get_next_agent(
        self, task: str, current_agent: str, result: str, completed_agents: List[str]
    ) -> Optional[str]:
        """让 LLM 决定下一个 Agent"""

        available = [a for a in config.agents.keys() if a not in completed_agents]

        if not available:
            return None

        prompt = f"""You are a task coordinator. Determine the next step.

Current Task: {task}
Current Agent: {current_agent}
Last Result: {result[:500]}...

Completed agents: {", ".join(completed_agents) if completed_agents else "None"}
Available agents: {", ".join(available)}

Based on the result, what should happen next?
Options:
- Use another agent from available list
- End the workflow if task is complete

Return ONLY:
- The next agent name (e.g., "frontend-dev") to continue
- "DONE" if the task is complete
Nothing else."""

        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            result_text = self._extract_response_content(response)

            if "DONE" in result_text.upper():
                return None

            matched_agent = self._extract_agent_name(result_text, available)
            if matched_agent:
                return matched_agent

            return None
        except Exception as e:
            logger.error(f"Router get_next_agent error: {e}", exc_info=True)
            return None
