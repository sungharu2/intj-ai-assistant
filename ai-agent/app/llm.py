import os

from dotenv import load_dotenv

load_dotenv()


def resolve_llm_provider() -> dict[str, object]:
    if os.getenv("GEMINI_API_KEY"):
        return {"provider": "gemini", "status": "configured"}
    if os.getenv("GROQ_API_KEY"):
        return {"provider": "groq", "status": "configured"}
    if os.getenv("OLLAMA_BASE_URL"):
        return {
            "provider": "ollama",
            "status": "configured",
            "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            "model": os.getenv("OLLAMA_MODEL", "llama3.2"),
        }
    return {"provider": "none", "status": "missing_credentials"}
