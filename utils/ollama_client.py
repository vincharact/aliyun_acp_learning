import os
from typing import Optional, List, Dict, Any
from ollama import Client


class OllamaClient:
    def __init__(
        self,
        model: str = "qwen3:8b",
        base_url: Optional[str] = None,
        timeout: int = 120
    ):
        self.model = model
        self.client = Client(
            host=base_url or os.getenv("OLLAMA_HOST", "http://localhost:11434"),
            timeout=timeout
        )

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        top_p: float = 0.9,
        stream: bool = False
    ) -> Dict[str, Any]:
        response = self.client.chat(
            model=self.model,
            messages=messages,
            options={
                "temperature": temperature,
                "top_p": top_p
            },
            stream=stream
        )
        return response

    def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        top_p: float = 0.9,
        stream: bool = False
    ) -> Dict[str, Any]:
        response = self.client.generate(
            model=self.model,
            prompt=prompt,
            options={
                "temperature": temperature,
                "top_p": top_p
            },
            stream=stream
        )
        return response

    def chat_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        top_p: float = 0.9
    ):
        response = self.client.chat(
            model=self.model,
            messages=messages,
            options={
                "temperature": temperature,
                "top_p": top_p
            },
            stream=True
        )
        return response

    def generate_stream(
        self,
        prompt: str,
        temperature: float = 0.7,
        top_p: float = 0.9
    ):
        response = self.client.generate(
            model=self.model,
            prompt=prompt,
            options={
                "temperature": temperature,
                "top_p": top_p
            },
            stream=True
        )
        return response

    def list_models(self) -> List[Dict[str, Any]]:
        return self.client.list()["models"]

    def pull_model(self, model_name: str) -> Dict[str, Any]:
        return self.client.pull(model_name)

    def show_model_info(self, model_name: Optional[str] = None) -> Dict[str, Any]:
        return self.client.show(model_name or self.model)
