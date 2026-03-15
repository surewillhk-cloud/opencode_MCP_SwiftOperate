import os
import logging
from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from .config import config

logger = logging.getLogger(__name__)


class ModelFactory:
    _instances: Dict[str, Any] = {}

    @classmethod
    def get_model(cls, model_name: str):
        if model_name in cls._instances:
            return cls._instances[model_name]

        model_cfg = config.get_model_config(model_name)
        if not model_cfg:
            model_cfg = {}
            provider_name = config.defaults.get("model", "openrouter").split("/")[0]
        else:
            provider_name = model_cfg.get("provider", "openrouter")

        provider_cfg = config.providers.get(provider_name, {})

        if provider_name == "openrouter":
            llm = ChatOpenAI(
                model=model_name,
                api_key=provider_cfg.get("api_key") or os.getenv("OPENROUTER_API_KEY"),
                base_url=provider_cfg.get("base_url", "https://openrouter.ai/api/v1"),
                temperature=model_cfg.get(
                    "temperature", config.defaults.get("temperature", 0.7)
                ),
                max_tokens=model_cfg.get(
                    "max_tokens", config.defaults.get("max_tokens", 4000)
                ),
                timeout=60,
            )
        elif provider_name == "openai":
            llm = ChatOpenAI(
                model=model_name,
                api_key=provider_cfg.get("api_key") or os.getenv("OPENAI_API_KEY"),
                base_url=provider_cfg.get("base_url"),
                temperature=model_cfg.get("temperature", 0.7),
            )
        elif provider_name == "anthropic":
            llm = ChatAnthropic(
                model=model_name,
                anthropic_api_key=provider_cfg.get("api_key")
                or os.getenv("ANTHROPIC_API_KEY"),
                temperature=model_cfg.get("temperature", 0.7),
                max_tokens_to_sample=model_cfg.get("max_tokens", 4000),
            )
        elif provider_name == "google":
            llm = ChatOpenAI(
                model=model_name,
                api_key=provider_cfg.get("api_key") or os.getenv("GOOGLE_API_KEY"),
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
                temperature=model_cfg.get("temperature", 0.7),
            )
        elif provider_name == "minimax":
            llm = ChatOpenAI(
                model=model_name,
                api_key=provider_cfg.get("api_key") or os.getenv("MINIMAX_API_KEY"),
                base_url=provider_cfg.get("base_url", "https://api.minimax.chat/v1"),
                temperature=model_cfg.get("temperature", 0.7),
            )
        elif provider_name == "nvidia":
            llm = ChatOpenAI(
                model=model_name,
                api_key=provider_cfg.get("api_key") or os.getenv("NVIDIA_API_KEY"),
                base_url=provider_cfg.get(
                    "base_url", "https://integrate.api.nvidia.com/v1"
                ),
                temperature=model_cfg.get("temperature", 0.7),
            )
        else:
            llm = ChatOpenAI(
                model=model_name,
                api_key=os.getenv("OPENROUTER_API_KEY"),
                base_url="https://openrouter.ai/api/v1",
                temperature=model_cfg.get("temperature", 0.7),
            )

        cls._instances[model_name] = llm
        return llm

    @classmethod
    def switch_model(cls, agent_name: str, new_model_name: str):
        agent_cfg = config.get_agent_config(agent_name)
        old_model = agent_cfg.get("model")
        if old_model and old_model in cls._instances:
            try:
                del cls._instances[old_model]
            except KeyError:
                logger.warning(f"Model {old_model} not in cache")
        agent_cfg["model"] = new_model_name
        return cls.get_model(new_model_name)

    @classmethod
    def get_current_model(cls, agent_name: str) -> str:
        agent_cfg = config.get_agent_config(agent_name)
        return agent_cfg.get("model", config.defaults.get("model"))

    @classmethod
    def clear_cache(cls):
        cls._instances.clear()
