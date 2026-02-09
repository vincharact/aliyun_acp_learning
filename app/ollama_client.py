import os
from typing import Optional, List, Dict, Any
from ollama import Client
import logging
import time

logger = logging.getLogger(__name__)


class OllamaClient:
    def __init__(
        self,
        model: str = "qwen3:8b",
        base_url: Optional[str] = None,
        timeout: int = 120
    ):
        self.model = model
        try:
            self.client = Client(
                host=base_url or os.getenv("OLLAMA_HOST", "http://localhost:11434"),
                timeout=timeout
            )
            logger.info(f"Ollama客户端初始化成功，模型: {model}, 地址: {base_url or os.getenv('OLLAMA_HOST', 'http://localhost:11434')}")
        except Exception as e:
            logger.error(f"Ollama客户端初始化失败: {e}")
            raise

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        top_p: float = 0.9,
        stream: bool = False,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        for attempt in range(max_retries):
            try:
                response = self.client.chat(
                    model=self.model,
                    messages=messages,
                    options={
                        "temperature": temperature,
                        "top_p": top_p
                    },
                    stream=stream
                )
                logger.debug(f"chat调用成功，消息数: {len(messages)}")
                return response
            except Exception as e:
                logger.warning(f"chat调用失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    logger.error(f"chat调用最终失败: {e}")
                    raise

    def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        top_p: float = 0.9,
        stream: bool = False,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        for attempt in range(max_retries):
            try:
                response = self.client.generate(
                    model=self.model,
                    prompt=prompt,
                    options={
                        "temperature": temperature,
                        "top_p": top_p
                    },
                    stream=stream
                )
                logger.debug(f"generate调用成功")
                return response
            except Exception as e:
                logger.warning(f"generate调用失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    logger.error(f"generate调用最终失败: {e}")
                    raise

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
        try:
            return self.client.list()["models"]
        except Exception as e:
            logger.error(f"列出模型失败: {e}")
            raise

    def pull_model(self, model_name: str) -> Dict[str, Any]:
        try:
            return self.client.pull(model_name)
        except Exception as e:
            logger.error(f"拉取模型失败: {e}")
            raise

    def show_model_info(self, model_name: Optional[str] = None) -> Dict[str, Any]:
        try:
            return self.client.show(model_name or self.model)
        except Exception as e:
            logger.error(f"获取模型信息失败: {e}")
            raise
