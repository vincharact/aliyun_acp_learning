from typing import Any, Dict, List, Optional
from langchain_core.language_models.llms import BaseLLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.outputs import Generation, LLMResult
from pydantic import Field
from utils.ollama_client import OllamaClient


class OllamaLLM(BaseLLM):
    client: OllamaClient = Field(...)
    temperature: float = Field(default=0.7)
    top_p: float = Field(default=0.9)

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
        generations = []
        for prompt in prompts:
            response = self.client.generate(
                prompt=prompt,
                temperature=self.temperature,
                top_p=self.top_p,
                stream=False
            )
            generations.append([Generation(text=response["response"])])
        return LLMResult(generations=generations)

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        return {
            "model": self.client.model,
            "temperature": self.temperature,
            "top_p": self.top_p,
        }
