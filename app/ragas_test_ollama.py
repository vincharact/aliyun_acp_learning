import sys

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import answer_correctness, context_precision, context_recall

from config import OllamaConfig, TestConfig
from factory import create_evaluation_components
from logger import logger
from utils import (
    create_dataset,
    create_simple_dataset,
    evaluate_with_metrics,
    print_separator,
)


def evaluate_answer_correctness(ollama_config: OllamaConfig = None, test_config: TestConfig = None):
    try:
        logger.info("开始评估答案准确度 (Answer Correctness)")
        _, llm, embeddings = create_evaluation_components(ollama_config)
        
        dataset = create_simple_dataset(test_config)
        result = evaluate_with_metrics(
            dataset=dataset,
            llm=llm,
            embeddings=embeddings,
            metrics=[answer_correctness]
        )
        
        logger.info("答案准确度评估完成")
        return result
    except Exception as e:
        logger.error(f"答案准确度评估失败: {e}")
        raise


def evaluate_retrieval_quality(ollama_config: OllamaConfig = None, test_config: TestConfig = None):
    try:
        logger.info("开始评估检索质量 (Context Recall & Context Precision)")
        _, llm, _ = create_evaluation_components(ollama_config)
        
        dataset = create_dataset(test_config)
        result = evaluate_with_metrics(
            dataset=dataset,
            llm=llm,
            metrics=[context_recall, context_precision]
        )
        
        logger.info("检索质量评估完成")
        return result
    except Exception as e:
        logger.error(f"检索质量评估失败: {e}")
        raise


def evaluate_full_pipeline(ollama_config: OllamaConfig = None, test_config: TestConfig = None):
    try:
        logger.info("开始完整评估 (Full Pipeline)")
        _, llm, embeddings = create_evaluation_components(ollama_config)
        
        dataset = create_dataset(test_config)
        result = evaluate_with_metrics(
            dataset=dataset,
            llm=llm,
            embeddings=embeddings,
            metrics=[answer_correctness, context_recall, context_precision]
        )
        
        logger.info("完整评估完成")
        return result
    except Exception as e:
        logger.error(f"完整评估失败: {e}")
        raise


if __name__ == "__main__":
    try:
        print_separator("评估答案准确度 (Answer Correctness)")
        result1 = evaluate_answer_correctness()
        print(result1)
        print()

        print_separator("评估检索质量 (Context Recall & Context Precision)")
        result2 = evaluate_retrieval_quality()
        print(result2)
        print()

        print_separator("完整评估 (Full Pipeline)")
        result3 = evaluate_full_pipeline()
        print(result3)
    except Exception as e:
        logger.error(f"测试执行失败: {e}")
        print(f"错误: {e}")
        sys.exit(1)
