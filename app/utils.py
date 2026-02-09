from typing import Any, Dict, List

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import answer_correctness, context_precision, context_recall

from config import TestConfig
from logger import logger


def create_dataset(test_config: TestConfig = None) -> Dataset:
    if test_config is None:
        test_config = TestConfig()
    
    test_config.validate()
    
    data_samples = {
        'question': test_config.questions,
        'answer': test_config.answers,
        'ground_truth': test_config.ground_truths,
        'contexts': test_config.contexts
    }
    
    return Dataset.from_dict(data_samples)


def create_simple_dataset(test_config: TestConfig = None) -> Dataset:
    if test_config is None:
        test_config = TestConfig()
    
    test_config.validate()
    
    data_samples = {
        'question': test_config.questions,
        'answer': test_config.answers,
        'ground_truth': test_config.ground_truths
    }
    
    return Dataset.from_dict(data_samples)


def evaluate_with_metrics(
    dataset: Dataset,
    llm,
    embeddings=None,
    metrics: List = None
) -> Any:
    if metrics is None:
        metrics = [answer_correctness, context_recall, context_precision]
    
    try:
        logger.info(f"开始评估，指标: {[m.name for m in metrics]}")
        
        if embeddings:
            score = evaluate(
                dataset=dataset,
                metrics=metrics,
                llm=llm,
                embeddings=embeddings
            )
        else:
            score = evaluate(
                dataset=dataset,
                metrics=metrics,
                llm=llm
            )
        
        logger.info("评估完成")
        return score.to_pandas()
    except Exception as e:
        logger.error(f"评估失败: {e}")
        raise


def print_separator(title: str = "", width: int = 80):
    print("=" * width)
    if title:
        print(title)
        print("=" * width)
