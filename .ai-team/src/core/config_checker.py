"""
Configuration Checker - 配置检查器

检查 API 配置状态，引导用户配置
"""

import os
from pathlib import Path
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()

API_KEYS = [
    "OPENROUTER_API_KEY",
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "GOOGLE_API_KEY",
    "MINIMAX_API_KEY",
    "NVIDIA_API_KEY",
]


def has_valid_api_key() -> bool:
    """检查是否有有效的 API Key"""
    for key in API_KEYS:
        value = os.getenv(key, "")
        placeholder = f"your-{key.lower().replace('_', '')}-key"
        if value and not value.startswith("your-") and len(value) > 10:
            return True
    return False


def get_configured_apis() -> Dict[str, str]:
    """获取已配置的 API"""
    configured = {}
    for key in API_KEYS:
        value = os.getenv(key, "")
        if value and value != f"your-{key.lower()}-key":
            configured[key] = value[:10] + "..." if len(value) > 10 else value
    return configured


def update_api_key(key_name: str, api_key: str) -> bool:
    """更新 API Key 到 .env 文件"""
    env_path = Path(__file__).parent.parent.parent / ".env"

    if not env_path.exists():
        return False

    with open(env_path, "r") as f:
        lines = f.readlines()

    updated = False
    new_lines = []
    for line in lines:
        if line.strip().startswith(f"{key_name}="):
            new_lines.append(f"{key_name}={api_key}\n")
            updated = True
        else:
            new_lines.append(line)

    if not updated:
        new_lines.append(f"{key_name}={api_key}\n")

    with open(env_path, "w") as f:
        f.writelines(new_lines)

    load_dotenv(env_path, override=True)
    return True


def get_available_providers() -> list:
    """获取可用的 providers"""
    configured = get_configured_apis()
    providers = []
    if "OPENROUTER_API_KEY" in configured:
        providers.append("OpenRouter")
    if "OPENAI_API_KEY" in configured:
        providers.append("OpenAI")
    if "ANTHROPIC_API_KEY" in configured:
        providers.append("Anthropic")
    if "GOOGLE_API_KEY" in configured:
        providers.append("Google")
    if "MINIMAX_API_KEY" in configured:
        providers.append("Minimax")
    return providers


def check_config_status() -> Dict[str, any]:
    """检查配置状态"""
    has_api = has_valid_api_key()
    configured = get_configured_apis()
    providers = get_available_providers()

    return {
        "has_valid_api": has_api,
        "configured_apis": configured,
        "available_providers": providers,
    }


def get_prompt_message() -> str:
    """获取配置引导提示信息"""
    status = check_config_status()

    if status["has_valid_api"]:
        return None

    msg = """【⚙️ API 配置检查】

我检测到你的 .env 还没有配置有效的 API Key。

支持的 API：
- OpenRouter (推荐，支持多种模型)
- OpenAI
- Anthropic
- Google
- Minimax
- Nvidia

请选择：
1. 提供 API Key，我帮你配置（例如：sk-or-v1-xxx）
2. 回复"没有"，使用当前 AI 直接执行任务

请回复你的选择或 API Key："""

    return msg


if __name__ == "__main__":
    status = check_config_status()
    print(f"Has valid API: {status['has_valid_api']}")
    print(f"Configured: {status['configured_apis']}")
    print(f"Providers: {status['available_providers']}")
