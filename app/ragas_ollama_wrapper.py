from typing import Any, Dict, List, Optional

from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import BaseLLM
from langchain_core.outputs import Generation, LLMResult
from pydantic import Field

from ollama_client import OllamaClient

from logger import logger


class OllamaLLM(BaseLLM):
    client: OllamaClient = Field(...)
    temperature: float = Field(default=0.7)
    top_p: float = Field(default=0.9)

    def __post_init__(self):
        if self.temperature < 0 or self.temperature > 2:
            raise ValueError("temperature must be between 0 and 2")
        if self.top_p < 0 or self.top_p > 1:
            raise ValueError("top_p must be between 0 and 1")

    @property
    def _llm_type(self) -> str:
        return "ollama"

    def _generate(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> LLMResult:
        if not prompts:
            logger.warning("_generate called with empty prompts list")
            return LLMResult(generations=[])
        
        try:
            generations = []
            for prompt in prompts:
                if not prompt:
                    logger.warning("empty prompt encountered, skipping")
                    continue
                    
                response = self.client.generate(
                    prompt=prompt,
                    temperature=self.temperature,
                    top_p=self.top_p,
                    stream=False
                )
                generations.append([Generation(text=response["response"])])
            
            logger.debug(f"生成完成，处理了 {len(prompts)} 个提示")
            return LLMResult(generations=generations)
        except Exception as e:
            logger.error(f"生成失败: {e}")
            raise

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        return {
            "model": self.client.model,
            "temperature": self.temperature,
            "top_p": self.top_p,
        }
