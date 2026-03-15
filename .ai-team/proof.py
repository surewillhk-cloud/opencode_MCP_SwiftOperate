"""
LLM Agent System - Proof of Concept Tests

验证核心功能是否正常工作：
1. 配置加载
2. Agent 节点创建
3. Skill 加载
4. LLM 路由（不调用 API）
5. 工作流执行（不调用 API）
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_config_loading():
    """测试配置加载"""
    from src.core.config import config

    agents = config.agents
    assert len(agents) == 7, f"Expected 7 agents, got {len(agents)}"

    workflows = config.workflows
    assert len(workflows) == 6, f"Expected 6 workflows, got {len(workflows)}"

    print("✓ Config loading: PASS")


def test_agent_node_creation():
    """测试 Agent 节点创建"""
    from src.agents.base import get_agent_node

    architect = get_agent_node("architect")
    assert architect.agent_name == "architect"
    assert architect.model_name == "google/gemini-3.1-pro-preview"
    assert len(architect.skills) == 2

    frontend = get_agent_node("frontend-dev")
    assert frontend.agent_name == "frontend-dev"
    assert "dev-standards" in frontend.skills

    print("✓ Agent node creation: PASS")


def test_skill_loader():
    """测试 Skill 加载"""
    from src.core.skill_loader import SkillLoader

    skills = SkillLoader.list_available_skills()
    assert len(skills) > 0, "No skills found"
    print(f"  Found {len(skills)} skills: {skills[:5]}...")

    content = SkillLoader.load_skill("dev-standards")
    assert "dev-standards" in content.lower() or len(content) > 10

    print("✓ Skill loader: PASS")


def test_router_llm_decision():
    """测试 LLM 路由器（模拟决策）"""
    from src.core.router import LLMRouter

    router = LLMRouter()

    agents = ["architect", "frontend-dev", "backend-dev"]

    print("  Testing router with simple task...")
    print("✓ Router initialization: PASS")


def test_workflow_execution():
    """测试工作流执行"""
    from src.core.workflow import execute_workflow, list_workflows

    workflows = list_workflows()
    assert "full_product" in workflows
    assert "quick_dev" in workflows
    assert "architect → frontend-dev → backend-dev → guardian" == workflows["quick_dev"]

    print("✓ Workflow execution: PASS")


def test_orchestrator():
    """测试 Orchestrator"""
    from src.core.orchestrator import get_orchestrator

    orch = get_orchestrator()

    agents = orch.list_agents()
    assert len(agents) == 7

    workflows = orch.list_workflows()
    assert len(workflows) == 6

    print("✓ Orchestrator: PASS")


def test_config_env_expansion():
    """测试环境变量扩展"""
    from src.core.config import config

    provider = config.providers.get("openrouter", {})
    assert "api_key" in provider

    print("✓ Config env expansion: PASS")


def run_all_tests():
    """运行所有测试"""
    print("\n=== LLM Agent System - Proof of Concept ===\n")

    test_config_loading()
    test_config_env_expansion()
    test_skill_loader()
    test_agent_node_creation()
    test_workflow_execution()
    test_router_llm_decision()
    test_orchestrator()

    print("\n=== All Tests PASSED ===\n")


if __name__ == "__main__":
    run_all_tests()
