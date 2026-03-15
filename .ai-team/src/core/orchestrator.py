from typing import Dict, Any, Optional, List
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from .config import config
from .router import LLMRouter
from .workflow import execute_workflow, list_workflows
from ..agents.base import get_agent_node, clear_agent_node_cache

logger = logging.getLogger(__name__)

MAX_CONTEXT_LENGTH = 8000


class AutoOrchestrator:
    """真正的 LLM 驱动 Orchestrator - 让 LLM 自主决策工作流"""

    def __init__(self):
        self.router = LLMRouter()
        self.max_iterations = 10

    @staticmethod
    def _truncate_context(task: str, max_length: int = MAX_CONTEXT_LENGTH) -> str:
        """截断过长的上下文"""
        if len(task) > max_length:
            return task[:max_length] + "\n... (truncated)"
        return task

    def execute(self, task: str, initial_agent: Optional[str] = None) -> Dict[str, Any]:
        """LLM 自主执行任务"""

        history = []
        completed_agents = []
        current_task = task
        iteration = 0

        if initial_agent:
            agent = get_agent_node(initial_agent)
            result = agent.execute(
                {
                    "task": current_task,
                    "context": {},
                    "history": history,
                    "iteration": iteration,
                }
            )

            history.extend(result.get("history", []))
            completed_agents.append(initial_agent)
            last_result = result.get("result", "")
            current_task = self._truncate_context(
                f"Previous result from {initial_agent}: {last_result}\n\nContinue: {task}"
            )
            iteration += 1

        while iteration < self.max_iterations:
            available_agents = [
                a for a in config.agents.keys() if a not in completed_agents
            ]

            if not available_agents:
                break

            next_agent = self.router.get_next_agent(
                task,
                completed_agents[-1] if completed_agents else "none",
                history[-1].get("content", "") if history else "",
                completed_agents,
            )

            if next_agent is None:
                break

            logger.info(f"[Auto] Selecting agent: {next_agent}")

            agent = get_agent_node(next_agent)
            result = agent.execute(
                {
                    "task": current_task,
                    "context": {"completed": completed_agents},
                    "history": history,
                    "iteration": iteration,
                }
            )

            history.extend(result.get("history", []))
            completed_agents.append(next_agent)

            last_result = result.get("result", "")
            current_task = self._truncate_context(
                f"Previous result from {next_agent}: {last_result}\n\nOriginal task: {task}"
            )
            iteration += 1

            should_continue = self.router.should_continue(task, last_result, history)
            if not should_continue:
                break

        return {
            "task": task,
            "result": history[-1].get("content", "") if history else "No result",
            "history": history,
            "completed_agents": completed_agents,
            "iteration": iteration,
        }

    def route_and_execute(self, task: str) -> Dict[str, Any]:
        """让 LLM 路由并执行"""

        available_agents = list(config.agents.keys())

        # LLM 决定第一个 Agent
        first_agent = self.router.route(task, available_agents)

        print(f"\n[Auto] First agent: {first_agent}")

        return self.execute(task, initial_agent=first_agent)


class WorkflowOrchestrator:
    """支持两种模式：LLM 驱动 + 预设工作流（带动态模型选择）"""

    def __init__(self):
        self.auto = AutoOrchestrator()
        self.dynamic_mode = True
        self.auto_confirm = False

    def execute(
        self, task: str, workflow_name: Optional[str] = None, auto: bool = False
    ) -> Dict[str, Any]:
        """执行任务 - 支持动态模型选择"""
        self.auto_confirm = auto

        if workflow_name:
            workflow_cfg = config.workflows.get(workflow_name)
            if not workflow_cfg:
                return {
                    "result": f"Workflow '{workflow_name}' not found",
                    "history": [],
                    "completed_agents": [],
                }

            steps = workflow_cfg.get("steps", [])
            if not steps:
                return {
                    "result": f"Workflow '{workflow_name}' has no steps",
                    "history": [],
                    "completed_agents": [],
                }

            if self.dynamic_mode:
                return self._execute_with_dynamic_models(task, workflow_name, steps)

            logger.info(f"Using workflow: {workflow_name} ({' → '.join(steps)})")
            return self._execute_steps(task, steps)

        return self.auto.route_and_execute(task)

    def _execute_with_dynamic_models(
        self, task: str, workflow_name: str, steps: List[str]
    ) -> Dict[str, Any]:
        """使用动态模型选择执行工作流"""
        from .complexity_analyzer import ComplexityAnalyzer
        from .dynamic_model_selector import DynamicModelSelector

        complexity_analysis = ComplexityAnalyzer.analyze(task)
        logger.info(
            f"Complexity analysis: {complexity_analysis.get('overall_level', 'medium')}"
        )

        model_selections = DynamicModelSelector.select_models(
            workflow_name, complexity_analysis
        )
        costs = DynamicModelSelector.estimate_cost(model_selections)

        report = DynamicModelSelector.format_selection_report(
            workflow_name, model_selections, complexity_analysis, costs
        )
        print(f"\n{report}")

        confirmed_selections = model_selections
        if not self.auto_confirm:
            user_input = input("").strip().lower()
            if user_input == "a":
                print("选择复杂度级别: low/medium/high/advanced")
                level = input("> ").strip().lower()
                if level in ["low", "medium", "high", "advanced"]:
                    confirmed_selections = DynamicModelSelector.adjust_models(
                        model_selections, level
                    )
                    costs = DynamicModelSelector.estimate_cost(confirmed_selections)
                    print(
                        f"已调整为 {level} 配置，预估成本: ${costs.get('total', 0):.2f}"
                    )
            elif user_input == "n":
                print("取消执行")
                return {
                    "result": "Cancelled by user",
                    "history": [],
                    "completed_agents": [],
                }

        for agent_name, model in confirmed_selections.items():
            config.update_agent_config(agent_name, {"model": model})
            logger.info(f"Dynamic model for {agent_name}: {model}")

        from .model_factory import ModelFactory

        ModelFactory._instances.clear()
        clear_agent_node_cache()

        logger.info(f"Using workflow: {workflow_name} ({' → '.join(steps)})")
        return self._execute_steps(task, steps, model_selections=confirmed_selections)

    def _execute_steps(
        self,
        task: str,
        steps: List[str],
        model_selections: Dict[str, str] | None = None,
        enable_research: bool = True,
    ) -> Dict[str, Any]:
        """按顺序执行多个 agent，支持并行阶段"""
        from .model_factory import ModelFactory
        from ..agents.base import get_agent_node

        if model_selections:
            for agent_name, model in model_selections.items():
                if agent_name in steps:
                    config.update_agent_config(agent_name, {"model": model})

        history = []
        completed_agents = []
        current_task = task

        research_context = {}
        if enable_research and "architect" in steps:
            logger.info("[Research] Starting concurrent research...")
            try:
                from .researcher import (
                    run_concurrent_research,
                    format_research_for_context,
                )

                research_results = run_concurrent_research(task)
                research_context = {"research": research_results}
                print(format_research_for_context(research_results))
            except Exception as e:
                logger.warning(f"Research failed: {e}, continuing without research")

        if steps and isinstance(steps[0], list):
            return self._execute_parallel_stages(task, steps, research_context)

        for step in steps:
            logger.info(f"[Workflow] Executing: {step}")

            context = {"completed": completed_agents}
            if research_context and step == "architect":
                context.update(research_context)

            agent = get_agent_node(step)
            try:
                result = agent.execute(
                    {
                        "task": current_task,
                        "context": context,
                        "history": history,
                        "iteration": 0,
                    }
                )
            except Exception as e:
                logger.error(f"Workflow step {step} failed: {e}", exc_info=True)
                return {
                    "result": f"Error in step {step}: {str(e)}",
                    "history": history,
                    "completed_agents": completed_agents,
                }

            history.extend(result.get("history", []))
            completed_agents.append(step)

            last_result = result.get("result", "")
            current_task = AutoOrchestrator._truncate_context(
                f"Previous result from {step}: {last_result}\n\nOriginal task: {task}"
            )

        return {
            "task": task,
            "result": history[-1].get("content", "") if history else "No result",
            "history": history,
            "completed_agents": completed_agents,
        }

    def _execute_parallel_stages(
        self,
        task: str,
        stages: List[List[str]],
        research_context: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        """并行执行多个阶段的 agent"""
        from ..agents.base import get_agent_node

        history = []
        completed_agents = []
        current_task = task

        for stage_idx, stage in enumerate(stages):
            if len(stage) == 1:
                logger.info(f"[Stage {stage_idx + 1}] Executing: {stage[0]}")

                context = {"completed": completed_agents}
                if research_context and stage[0] == "architect":
                    context.update(research_context)

                agent = get_agent_node(stage[0])
                result = agent.execute(
                    {
                        "task": current_task,
                        "context": context,
                        "history": history,
                        "iteration": 0,
                    }
                )

                history.extend(result.get("history", []))
                completed_agents.append(stage[0])
                last_result = result.get("result", "")
                current_task = AutoOrchestrator._truncate_context(
                    f"Previous results: {last_result}\n\nOriginal task: {task}"
                )
            else:
                logger.info(f"[Stage {stage_idx + 1}] Parallel execution: {stage}")

                def execute_agent(
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

                context = {"completed": completed_agents}

                with ThreadPoolExecutor(max_workers=len(stage)) as executor:
                    futures = {
                        executor.submit(
                            execute_agent, agent_name, current_task, context, history
                        ): agent_name
                        for agent_name in stage
                    }

                    stage_results = {}
                    for future in as_completed(futures):
                        agent_name = futures[future]
                        try:
                            result = future.result()
                            stage_results[agent_name] = result
                            history.extend(result.get("history", []))
                            completed_agents.append(agent_name)
                            logger.info(f"[Parallel] {agent_name} completed")
                        except Exception as e:
                            logger.error(f"[Parallel] {agent_name} failed: {e}")
                            stage_results[agent_name] = {
                                "result": f"Error: {e}",
                                "history": [],
                            }

                combined_results = "\n\n".join(
                    [
                        f"=== {name} ===\n{r.get('result', '')}"
                        for name, r in stage_results.items()
                    ]
                )
                current_task = AutoOrchestrator._truncate_context(
                    f"Previous parallel results:\n{combined_results}\n\nOriginal task: {task}"
                )

        return {
            "task": task,
            "result": history[-1].get("content", "") if history else "No result",
            "history": history,
            "completed_agents": completed_agents,
        }

    def _execute_legacy(self, task: str, workflow_name: str) -> Dict[str, Any]:
        """传统预设工作流（保留兼容）"""
        return execute_workflow(task, workflow_name)

    def list_agents(self) -> Dict[str, Any]:
        """列出所有 Agent"""
        return {
            name: {
                "model": cfg.get("model", "unknown"),
                "description": cfg.get("description", ""),
                "skills": cfg.get("skills", []),
            }
            for name, cfg in config.agents.items()
        }

    def list_workflows(self) -> Dict[str, str]:
        """列出所有工作流"""
        return list_workflows()

    def route_task(self, task: str) -> str:
        """路由任务到合适的 Agent"""
        available_agents = list(config.agents.keys())
        return self.auto.router.route(task, available_agents)

    def switch_agent_model(self, agent_name: str, new_model: str) -> None:
        """切换 Agent 的模型"""
        from .model_factory import ModelFactory

        config.update_agent_config(agent_name, {"model": new_model})
        ModelFactory._instances.clear()
        clear_agent_node_cache(agent_name)
        logger.info(f"Switched {agent_name} to {new_model}")


_orchestrator: Optional[WorkflowOrchestrator] = None


def get_orchestrator() -> WorkflowOrchestrator:
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = WorkflowOrchestrator()
    return _orchestrator
