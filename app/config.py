from dataclasses import dataclass
from typing import Optional


@dataclass
class OllamaConfig:
    model: str = "qwen3:8b"
    base_url: Optional[str] = None
    timeout: int = 120
    temperature: float = 0.7
    top_p: float = 0.9


@dataclass
class TestConfig:
    questions: list = None
    answers: list = None
    ground_truths: list = None
    contexts: list = None

    def __post_init__(self):
        if self.questions is None:
            self.questions = [
                '张伟是哪个部门的？',
                '张伟是哪个部门的？',
                '张伟是哪个部门的？'
            ]
        if self.answers is None:
            self.answers = [
                '根据提供的信息，没有提到张伟所在的部门。如果您能提供更多关于张伟的信息，我可能能够帮助您找到答案。',
                '张伟是人事部门的',
                '张伟是教研部的'
            ]
        if self.ground_truths is None:
            self.ground_truths = [
                '张伟是教研部的成员',
                '张伟是教研部的成员',
                '张伟是教研部的成员'
            ]
        if self.contexts is None:
            self.contexts = [
                ['提供⾏政管理与协调⽀持，优化⾏政⼯作流程。 ', '绩效管理部 韩杉 李⻜ I902 041 ⼈⼒资源'],
                ['李凯 教研部主任 ', '牛顿发现了万有引力'],
                ['牛顿发现了万有引力', '张伟 教研部工程师，他最近在负责课程研发'],
            ]
