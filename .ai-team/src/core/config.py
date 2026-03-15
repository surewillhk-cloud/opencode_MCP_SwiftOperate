import os
import copy
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()


class Config:
    _instance = None
    _config: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        config_path = Path(__file__).parent.parent.parent / "config" / "agents.yaml"
        with open(config_path, "r") as f:
            self._config = yaml.safe_load(f)
        self._expand_env_vars(self._config)

    def _expand_env_vars(self, obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if (
                    isinstance(value, str)
                    and value.startswith("${")
                    and value.endswith("}")
                ):
                    env_var = value[2:-1]
                    obj[key] = os.getenv(env_var, value)
                elif isinstance(value, (dict, list)):
                    self._expand_env_vars(value)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                if (
                    isinstance(item, str)
                    and item.startswith("${")
                    and item.endswith("}")
                ):
                    obj[i] = os.getenv(item[2:-1], item)
                elif isinstance(item, (dict, list)):
                    self._expand_env_vars(item)

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split(".")
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            if value is None:
                return default
        return value

    @property
    def defaults(self) -> Dict[str, Any]:
        return self._config.get("defaults", {})

    @property
    def providers(self) -> Dict[str, Any]:
        return self._config.get("providers", {})

    @property
    def models(self) -> Dict[str, Any]:
        return self._config.get("models", {})

    @property
    def agents(self) -> Dict[str, Any]:
        return self._config.get("agents", {})

    @property
    def workflows(self) -> Dict[str, Any]:
        return self._config.get("workflows", {})

    def get_agent_config(self, agent_name: str) -> Dict[str, Any]:
        return copy.deepcopy(self.agents.get(agent_name, {}))

    def get_model_config(self, model_name: str) -> Dict[str, Any]:
        return copy.deepcopy(self.models.get(model_name, {}))

    def reload(self):
        self._load_config()

    def update_agent_config(self, agent_name: str, updates: Dict[str, Any]) -> None:
        if agent_name in self._config.get("agents", {}):
            self._config["agents"][agent_name].update(updates)

    def validate(self) -> list:
        """验证配置，返回警告列表"""
        warnings = []

        for agent_name, agent_cfg in self.agents.items():
            model = agent_cfg.get("model")
            if model and model not in self.models:
                warnings.append(
                    f"Agent '{agent_name}' uses model '{model}' not defined in models config"
                )

            md_path = agent_cfg.get("agent_md_path")
            if md_path:
                full_path = Path(__file__).parent.parent.parent / md_path
                if not full_path.exists():
                    warnings.append(
                        f"Agent '{agent_name}' md file not found: {md_path}"
                    )

        router_model = self.defaults.get("router_model")
        if router_model and router_model not in self.models:
            warnings.append(
                f"Router model '{router_model}' not defined in models config"
            )

        return warnings


config = Config()
