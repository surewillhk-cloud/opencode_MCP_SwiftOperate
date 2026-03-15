from typing import Dict, List, Optional
from pathlib import Path


class SkillLoader:
    """Skill 加载器 - 从 opencode-agent-skill 加载 Skill"""

    SKILL_BASE_PATH = (
        Path(__file__).parent.parent.parent
        / "opencode-agent-skill"
        / ".opencode"
        / "skills"
    )

    _skill_cache: Dict[str, str] = {}

    @classmethod
    def load_skill(cls, skill_name: str) -> str:
        """加载 Skill 内容"""
        if skill_name in cls._skill_cache:
            return cls._skill_cache[skill_name]

        skill_path = cls.SKILL_BASE_PATH / skill_name / "SKILL.md"

        if not skill_path.exists():
            return f"Skill '{skill_name}' not found"

        with open(skill_path, "r") as f:
            content = f.read()

        cls._skill_cache[skill_name] = content
        return content

    @classmethod
    def load_skills(cls, skill_names: List[str]) -> str:
        """加载多个 Skill 并合并"""
        if not skill_names:
            return ""

        skills_content = ["## Loaded Skills\n"]
        for name in skill_names:
            content = cls.load_skill(name)
            skills_content.append(f"\n### Skill: {name}\n")
            skills_content.append(content)
            skills_content.append("\n---\n")

        return "\n".join(skills_content)

    @classmethod
    def list_available_skills(cls) -> List[str]:
        """列出所有可用的 Skill"""
        if not cls.SKILL_BASE_PATH.exists():
            return []

        skills = []
        for item in cls.SKILL_BASE_PATH.iterdir():
            if item.is_dir() and (item / "SKILL.md").exists():
                skills.append(item.name)
        return skills


def get_skill_content(skill_name: str) -> str:
    """便捷函数：获取 Skill 内容"""
    return SkillLoader.load_skill(skill_name)


def get_skills_content(skill_names: List[str]) -> str:
    """便捷函数：获取多个 Skill 内容"""
    return SkillLoader.load_skills(skill_names)
