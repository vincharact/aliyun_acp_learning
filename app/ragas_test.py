import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import answer_correctness, context_recall, context_precision
from app.config import OllamaConfig, TestConfig
from app.factory import create_ollama_components


def create_dataset(test_config: TestConfig = None):
    if test_config is None:
        test_config = TestConfig()
    
    data_samples = {
        'question': test_config.questions,
        'answer': test_config.answers,
        'ground_truth': test_config.ground_truths,
        'contexts': test_config.contexts
    }
    
    return Dataset.from_dict(data_samples)


def evaluate_answer_correctness(ollama_config: OllamaConfig = None, test_config: TestConfig = None):
    _, llm, embeddings = create_ollama_components(ollama_config)
    
    data_samples = {
        'question': test_config.questions if test_config else TestConfig().questions,
        'answer': test_config.answers if test_config else TestConfig().answers,
        'ground_truth': test_config.ground_truths if test_config else TestConfig().ground_truths
    }
    
    dataset = Dataset.from_dict(data_samples)
    score = evaluate(
        dataset=dataset,
        metrics=[answer_correctness],
        llm=llm,
        embeddings=embeddings
    )
    return score.to_pandas()


def evaluate_retrieval_quality(ollama_config: OllamaConfig = None, test_config: TestConfig = None):
    _, llm, _ = create_ollama_components(ollama_config)
    
    dataset = create_dataset(test_config)
    score = evaluate(
        dataset=dataset,
        metrics=[context_recall, context_precision],
        llm=llm
    )
    return score.to_pandas()


def evaluate_full_pipeline(ollama_config: OllamaConfig = None, test_config: TestConfig = None):
    _, llm, embeddings = create_ollama_components(ollama_config)
    
    dataset = create_dataset(test_config)
    score = evaluate(
        dataset=dataset,
        metrics=[answer_correctness, context_recall, context_precision],
        llm=llm,
        embeddings=embeddings
    )
    return score.to_pandas()


if __name__ == "__main__":
    print("=" * 80)
    print("评估答案准确度 (Answer Correctness)")
    print("=" * 80)
    result1 = evaluate_answer_correctness()
    print(result1)
    print()

    print("=" * 80)
    print("评估检索质量 (Context Recall & Context Precision)")
    print("=" * 80)
    result2 = evaluate_retrieval_quality()
    print(result2)
    print()

    print("=" * 80)
    print("完整评估 (Full Pipeline)")
    print("=" * 80)
    result3 = evaluate_full_pipeline()
    print(result3)
