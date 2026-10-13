from fastapi import FastAPI

from app.graph.state import AgentState
from app.llm import resolve_llm_provider

app = FastAPI(title="INTJ AI Agent", version="0.1.0")


@app.get("/health")
def health() -> dict[str, object]:
    return {
        "status": "UP",
        "service": "ai-agent",
        "llm": resolve_llm_provider(),
        "state_keys": list(AgentState.__annotations__.keys()),
    }
