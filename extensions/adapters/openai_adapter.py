from typing import Iterable, Dict, Optional
import os

class OpenAIBackend:
    def __init__(self, model: str="gpt-4o-mini", api_key: Optional[str]=None, base_url: Optional[str]=None):
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY not set.")
        # Lazy import to avoid hard dependency when not used
        import requests  # noqa: F401

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def generate(self, prompt: str, *, system: Optional[str]=None, max_tokens: int=512, temperature: float=0.7, stream: bool=False, **kw) -> str:
        import requests, json
        url = f"{self.base_url}/chat/completions"
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": False,
        }
        r = requests.post(url, headers=self._headers(), json=payload, timeout=60)
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"].strip()

    def generate_chat(self, messages: Iterable[Dict[str, str]], *, max_tokens: int=512, temperature: float=0.7, stream: bool=False, **kw) -> str:
        import requests, json
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": self.model,
            "messages": list(messages),
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": False,
        }
        r = requests.post(url, headers=self._headers(), json=payload, timeout=60)
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"].strip()
