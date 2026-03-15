from typing import Callable, Dict, Any, List
import json
from pathlib import Path
import logging
from langchain_core.messages import HumanMessage, SystemMessage

from ..core.config import config
from ..core.model_factory import ModelFactory
from ..core.skill_loader import get_skills_content

logger = logging.getLogger(__name__)

MAX_HISTORY_LENGTH = 10
MAX_CONTEXT_LENGTH = 4000


def load_agent_md(agent_name: str) -> str:
    """加载 Agent MD 文件内容"""
    agent_cfg = config.get_agent_config(agent_name)
    md_path = agent_cfg.get("agent_md_path")

    if not md_path:
        return f"You are {agent_name}."

    full_path = Path(__file__).parent.parent.parent / md_path

    if not full_path.exists():
        return f"You are {agent_name}."

    with open(full_path, "r") as f:
        content = f.read()

    lines = content.split("\n")
    start = 0
    for i, line in enumerate(lines):
        if line.strip() and not line.startswith("#") and not line.startswith("---"):
            start = i
            break

    return "\n".join(lines[start:])


class LLMAgentNode:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.agent_cfg = config.get_agent_config(agent_name)
        self.model_name = self.agent_cfg.get("model", config.defaults.get("model"))
        self.max_iterations = self.agent_cfg.get("max_iterations", 5)
        self.skills = self.agent_cfg.get("skills", [])
        self._system_prompt = None
        self._llm = None

    @property
    def system_prompt(self):
        if self._system_prompt is None:
            base_prompt = load_agent_md(self.agent_name)
            skills_content = get_skills_content(self.skills)
            self._system_prompt = f"{base_prompt}\n\n{skills_content}"
        return self._system_prompt

    @property
    def llm(self):
        if self._llm is None:
            self._llm = ModelFactory.get_model(self.model_name)
        return self._llm

    def execute(self, state: dict) -> dict:
        task = state.get("task", "")
        context = state.get("context", {})
        history = state.get("history", [])
        iteration = state.get("iteration", 0)

        if iteration >= self.max_iterations:
            return {
                "result": f"Max iterations reached for {self.agent_name}",
                "iteration": iteration + 1,
            }

        messages = [SystemMessage(content=self.system_prompt)]

        recent_history = history[-MAX_HISTORY_LENGTH:]
        for msg in recent_history:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "user":
                messages.append(HumanMessage(content=content))
            else:
                messages.append(SystemMessage(content=content))

        context_str = self._serialize_context(context)
        if context_str:
            messages.append(
                HumanMessage(content=f"Context:\n{context_str}\n\nTask: {task}")
            )
        else:
            messages.append(HumanMessage(content=task))

        try:
            response = self.llm.invoke(messages)
            result = response.content if hasattr(response, "content") else str(response)
        except Exception as e:
            logger.error(f"Agent {self.agent_name} execution error: {e}", exc_info=True)
            result = f"Error: {str(e)}"

        new_history = history + [
            {"role": "user", "content": task},
            {"role": "assistant", "content": result},
        ]

        return {
            "result": result,
            "current_agent": self.agent_name,
            "history": new_history,
            "iteration": iteration + 1,
            "context": {**context, "last_result": result},
        }

    def _serialize_context(self, context: Dict[str, Any]) -> str:
        """安全序列化 context 为字符串"""
        if not context:
            return ""

        lines = []
        for k, v in context.items():
            if isinstance(v, (dict, list)):
                lines.append(f"{k}: {json.dumps(v, ensure_ascii=False)[:500]}")
            else:
                v_str = str(v)
                if len(v_str) > MAX_CONTEXT_LENGTH:
                    v_str = v_str[:MAX_CONTEXT_LENGTH] + "..."
                lines.append(f"{k}: {v_str}")
        return "\n".join(lines)

    def switch_model(self, new_model_name: str):
        self._llm = ModelFactory.switch_model(self.agent_name, new_model_name)
        self.model_name = new_model_name
        return self._llm

    def get_current_model(self) -> str:
        return self.model_name


_agent_nodes: Dict[str, LLMAgentNode] = {}


def get_agent_node(agent_name: str) -> LLMAgentNode:
    if agent_name not in _agent_nodes:
        _agent_nodes[agent_name] = LLMAgentNode(agent_name)
    return _agent_nodes[agent_name]


def clear_agent_node_cache(agent_name: str = None):
    """清除 Agent 节点缓存"""
    global _agent_nodes
    if agent_name:
        if agent_name in _agent_nodes:
            del _agent_nodes[agent_name]
            logger.info(f"Cleared cache for agent: {agent_name}")
    else:
        _agent_nodes.clear()
        logger.info("Cleared all agent caches")


def create_agent_node(agent_name: str) -> Callable:
    def node(state: dict) -> dict:
        agent = get_agent_node(agent_name)
        return agent.execute(state)

    return node
