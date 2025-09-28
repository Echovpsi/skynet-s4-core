"""Generic LLM adapter used OUT-OF-TREE to avoid touching existing code.
Usage example inside your own scripts:

    from extensions.llm_adapter import generate, set_backend
    set_backend("openai", model="gpt-4o-mini")
    print(generate("Hello"))

This file intentionally does not alter app/main.py. If you wish to wire it,
import and use in your own orchestrator or extend app via a separate blueprint.
"""
from typing import Optional, Dict, Any, Iterable
import os

_BACKEND = None
_BACKEND_NAME = None

def set_backend(name: str, **kwargs):
    global _BACKEND, _BACKEND_NAME
    name = name.lower()
    if name == "openai":
        from .adapters.openai_adapter import OpenAIBackend
        _BACKEND = OpenAIBackend(**kwargs)
        _BACKEND_NAME = name
    elif name in ("ollama", "local"):
        from .adapters.local_ollama_adapter import OllamaBackend
        _BACKEND = OllamaBackend(**kwargs)
        _BACKEND_NAME = name
    else:
        raise ValueError(f"Unknown backend: {name}")

def backend_name() -> Optional[str]:
    return _BACKEND_NAME

def generate(prompt: str, *, system: Optional[str]=None, max_tokens: int=512, temperature: float=0.7, stream: bool=False, **kw) -> str:
    if _BACKEND is None:
        raise RuntimeError("LLM backend not configured. Call set_backend(...) first.")
    return _BACKEND.generate(prompt, system=system, max_tokens=max_tokens, temperature=temperature, stream=stream, **kw)

def generate_chat(messages: Iterable[Dict[str, str]], *, max_tokens: int=512, temperature: float=0.7, stream: bool=False, **kw) -> str:
    if _BACKEND is None:
        raise RuntimeError("LLM backend not configured. Call set_backend(...) first.")
    return _BACKEND.generate_chat(messages, max_tokens=max_tokens, temperature=temperature, stream=stream, **kw)
