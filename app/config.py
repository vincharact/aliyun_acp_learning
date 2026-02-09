from dataclasses import dataclass, field
from typing import Optional, List


DEFAULT_OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_TIMEOUT = 120
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_P = 0.9

DEFAULT_THINKING_MODEL = "qwen3:8b"
DEFAULT_NON_THINKING_MODEL = "qwen2.5:14b"
DEFAULT_EMBEDDING_MODEL = "bge-m3:latest"
DEFAULT_RERANK_MODEL = "qllama/bge-reranker-v2-m3:latest"


@dataclass
class OllamaConfig:
    thinking_model: str = DEFAULT_THINKING_MODEL
    non_thinking_model: str = DEFAULT_NON_THINKING_MODEL
    embedding_model: str = DEFAULT_EMBEDDING_MODEL
    rerank_model: str = DEFAULT_RERANK_MODEL
    base_url: Optional[str] = DEFAULT_OLLAMA_BASE_URL
    timeout: int = DEFAULT_TIMEOUT
    temperature: float = DEFAULT_TEMPERATURE
    top_p: float = DEFAULT_TOP_P

    def __post_init__(self):
        if self.temperature < 0 or self.temperature > 2:
            raise ValueError("temperature must be between 0 and 2")
        if self.top_p < 0 or self.top_p > 1:
            raise ValueError("top_p must be between 0 and 1")
        if self.timeout <= 0:
            raise ValueError("timeout must be positive")


@dataclass
class TestConfig:
    questions: List[str] = field(default_factory=list)
    answers: List[str] = field(default_factory=list)
    ground_truths: List[str] = field(default_factory=list)
    contexts: List[List[str]] = field(default_factory=list)

    def __post_init__(self):
        if not self.questions:
            self.questions = [
                '张伟是哪个部门的？',
                '张伟是哪个部门的？',
                '张伟是哪个部门的？'
            ]
        if not self.answers:
            self.answers = [
                '根据提供的信息，没有提到张伟所在的部门。如果您能提供更多关于张伟的信息，我可能能够帮助您找到答案。',
                '张伟是人事部门的',
                '张伟是教研部的'
            ]
        if not self.ground_truths:
            self.ground_truths = [
                '张伟是教研部的成员',
                '张伟是教研部的成员',
                '张伟是教研部的成员'
            ]
        if not self.contexts:
            self.contexts = [
                ['提供⾏政管理与协调⽀持，优化⾏政⼯作流程。 ', '绩效管理部 韩杉 李⻜ I902 041 ⼈⼒资源'],
                ['李凯 教研部主任 ', '牛顿发现了万有引力'],
                ['牛顿发现了万有引力', '张伟 教研部工程师，他最近在负责课程研发'],
            ]

    def validate(self) -> bool:
        if len(self.questions) != len(self.answers):
            raise ValueError("questions and answers must have the same length")
        if len(self.questions) != len(self.ground_truths):
            raise ValueError("questions and ground_truths must have the same length")
        if self.contexts and len(self.questions) != len(self.contexts):
            raise ValueError("questions and contexts must have the same length")
        return True
