from typing import Any, TypedDict


class AgentState(TypedDict, total=False):
    user_id: str | None
    request: str
    schedule_data: Any
    intent: str | None
    plan: Any
    result: Any
