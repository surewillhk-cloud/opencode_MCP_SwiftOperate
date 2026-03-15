"""
LLM Agent System - Entry Point

Usage:
    python main.py                    # Interactive mode
    python main.py "your task"       # Execute task
    python main.py --list-agents     # List all agents
    python main.py --list-skills      # List all skills
"""

import sys
import argparse
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

from src.core.orchestrator import get_orchestrator
from src.core.config import config
from src.core.skill_loader import SkillLoader
from src.utils.banner import print_banner


def main():
    print_banner()
    parser = argparse.ArgumentParser(description="LLM Agent System")
    parser.add_argument("task", nargs="?", help="Task description")
    parser.add_argument("--agent", "-a", help="Specify agent")
    parser.add_argument("--workflow", "-w", help="Specify workflow")
    parser.add_argument(
        "--list-agents", "-l", action="store_true", help="List all agents"
    )
    parser.add_argument("--list-skills", action="store_true", help="List all skills")
    parser.add_argument(
        "--list-workflows", action="store_true", help="List all workflows"
    )
    parser.add_argument(
        "--switch", nargs=2, metavar=("AGENT", "MODEL"), help="Switch agent model"
    )
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Auto confirm model selection without prompting",
    )
    parser.add_argument(
        "--no-dynamic", action="store_true", help="Disable dynamic model selection"
    )

    args = parser.parse_args()

    orchestrator = get_orchestrator()

    if args.list_agents:
        print("\n=== Agents (7) ===")
        agents = orchestrator.list_agents()
        for name, info in agents.items():
            print(f"\n[{name}]")
            print(f"  Model: {info['model']}")
            print(f"  Description: {info['description']}")
            print(f"  Skills: {', '.join(info['skills'])}")
        return

    if args.list_skills:
        print("\n=== Available Skills ===")
        skills = SkillLoader.list_available_skills()
        for skill in sorted(skills):
            print(f"  - {skill}")
        return

    if args.list_workflows:
        print("\n=== Workflows ===")
        workflows = orchestrator.list_workflows()
        for name, desc in workflows.items():
            print(f"\n[{name}]")
            print(f"  {desc}")
        return

    if args.switch:
        agent_name, new_model = args.switch
        try:
            orchestrator.switch_agent_model(agent_name, new_model)
            print(f"✓ {agent_name} switched to {new_model}")
        except Exception as e:
            print(f"✗ Error: {e}")
        return

    orchestrator.dynamic_mode = not args.no_dynamic

    if args.task:
        workflow_name = args.workflow
        if not workflow_name:
            workflow_name = "quick_dev"
            print(f"\n[Route] No workflow specified, using default: {workflow_name}")

        result = orchestrator.execute(args.task, workflow_name, auto=args.auto)
        print(f"\n=== Result ===")
        print(result.get("result", ""))
    else:
        print("\n=== LLM Agent System ===")
        print("Interactive mode (type 'quit' to exit)\n")

        while True:
            try:
                task = input("> ")
                if task.lower() in ["quit", "exit", "q"]:
                    break
                if not task.strip():
                    continue

                workflow_name = "quick_dev"
                print(f"[Route] Using default workflow: {workflow_name}")

                result = orchestrator.execute(task, workflow_name, auto=args.auto)
                print(f"\n{result.get('result', '')}\n")
            except KeyboardInterrupt:
                break
            except EOFError:
                print("\nExiting...")
                break
            except Exception as e:
                logging.error(f"Error executing task: {e}", exc_info=True)
                print(f"Error: {e}")


if __name__ == "__main__":
    main()
