from typing import TypedDict, List


class AgentState(TypedDict):
    task: str
    current_agent: str
    context: dict
    result: str
    history: List[dict]
    iteration: int
