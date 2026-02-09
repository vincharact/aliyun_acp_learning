import sys

from config import OllamaConfig, TestConfig
from logger import logger
from ragas_test_ollama import (
    evaluate_answer_correctness,
    evaluate_full_pipeline,
    evaluate_retrieval_quality,
)
from utils import print_separator


def main():
    try:
        ollama_config = OllamaConfig(
            thinking_model="qwen2.5:14b",
            non_thinking_model="qwen2.5:14b",
            embedding_model="bge-m3:latest",
            rerank_model="qllama/bge-reranker-v2-m3:latest",
            base_url="http://localhost:11434",
            timeout=120,
            temperature=0.7,
            top_p=0.9
        )
        
        test_config = TestConfig(
            questions=[
                '张伟是哪个部门的？',
                '张伟是哪个部门的？',
                '张伟是哪个部门的？'
            ],
            answers=[
                '根据提供的信息，没有提到张伟所在的部门。如果您能提供更多关于张伟的信息，我可能能够帮助您找到答案。',
                '张伟是人事部门的',
                '张伟是教研部的'
            ],
            ground_truths=[
                '张伟是教研部的成员',
                '张伟是教研部的成员',
                '张伟是教研部的成员'
            ],
            contexts=[
                ['提供⾏政管理与协调⽀持，优化⾏政⼯作流程。 ', '绩效管理部 韩杉 李⻜ I902 041 ⼈⼒资源'],
                ['李凯 教研部主任 ', '牛顿发现了万有引力'],
                ['牛顿发现了万有引力', '张伟 教研部工程师，他最近在负责课程研发'],
            ]
        )
        
        print_separator("RAG系统自动化评估 - 使用本地Ollama模型")
        print(f"模型: {ollama_config.non_thinking_model}")
        print(f"地址: {ollama_config.base_url}")
        print_separator()
        print()
        
        print_separator("1. 评估答案准确度 (Answer Correctness)")
        result1 = evaluate_answer_correctness(ollama_config, test_config)
        print(result1)
        print()
        
        print_separator("2. 评估检索质量 (Context Recall & Context Precision)")
        result2 = evaluate_retrieval_quality(ollama_config, test_config)
        print(result2)
        print()
        
        print_separator("3. 完整评估 (Full Pipeline)")
        result3 = evaluate_full_pipeline(ollama_config, test_config)
        print(result3)
        print()
        
        print_separator("评估完成！")
        
    except Exception as e:
        logger.error(f"主程序执行失败: {e}")
        print(f"错误: {e}")
        print("\n请确保：")
        print("1. Ollama服务已启动 (ollama serve)")
        print("2. 指定的模型已下载 (ollama pull qwen3:8b)")
        print("3. 网络连接正常")
        sys.exit(1)


if __name__ == "__main__":
    main()
