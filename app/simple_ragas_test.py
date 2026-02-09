import sys
import traceback

from ragas.metrics import answer_correctness

from config import OllamaConfig, TestConfig
from factory import create_evaluation_components
from logger import logger
from utils import create_simple_dataset, evaluate_with_metrics, print_separator


def simple_test():
    try:
        logger.info("开始简单测试...")
        
        ollama_config = OllamaConfig()
        
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
            ]
        )
        
        logger.info("创建Ollama组件...")
        _, llm, embeddings = create_evaluation_components(ollama_config)
        
        logger.info("创建测试数据集...")
        dataset = create_simple_dataset(test_config)
        logger.info(f"数据集大小: {len(dataset)}")
        
        logger.info("开始评估...")
        score = evaluate_with_metrics(
            dataset=dataset,
            llm=llm,
            embeddings=embeddings,
            metrics=[answer_correctness]
        )
        
        logger.info("评估完成！")
        print("\n评估结果:")
        print(score)
        
        return True
        
    except Exception as e:
        logger.error(f"测试失败: {e}")
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = simple_test()
    if success:
        print("\n✅ 测试成功！")
        sys.exit(0)
    else:
        print("\n❌ 测试失败！")
        sys.exit(1)
