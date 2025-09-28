from typing import Iterable, Dict, Optional
import os, json

class OllamaBackend:
    def __init__(self, model: str="mistral", base_url: Optional[str]=None):
        self.model = model
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    def generate(self, prompt: str, *, system: Optional[str]=None, max_tokens: int=512, temperature: float=0.7, stream: bool=False, **kw) -> str:
        import requests
        url = f"{self.base_url}/api/chat"
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        payload = {"model": self.model, "messages": messages, "options": {"temperature": temperature}}
        r = requests.post(url, json=payload, timeout=60)
        r.raise_for_status()
        # Ollama can stream; here we keep it simple (non-stream aggregation)
        data = r.json()
        if isinstance(data, dict) and "message" in data:
            return data["message"].get("content", "").strip()
        # Some versions return stream of lines
        if isinstance(data, list):
            txt = ""
            for item in data:
                msg = item.get("message", {}).get("content", "")
                txt += msg
            return txt.strip()
        return ""

    def generate_chat(self, messages: Iterable[Dict[str, str]], *, max_tokens: int=512, temperature: float=0.7, stream: bool=False, **kw) -> str:
        import requests
        url = f"{self.base_url}/api/chat"
        payload = {"model": self.model, "messages": list(messages), "options": {"temperature": temperature}}
        r = requests.post(url, json=payload, timeout=60)
        r.raise_for_status()
        data = r.json()
        if isinstance(data, dict) and "message" in data:
            return data["message"].get("content", "").strip()
        if isinstance(data, list):
            txt = ""
            for item in data:
                msg = item.get("message", {}).get("content", "")
                txt += msg
            return txt.strip()
        return ""
