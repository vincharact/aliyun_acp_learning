import sys
import traceback

from config import OllamaConfig, TestConfig
from factory import create_ollama_components
from logger import logger


def test_components():
    try:
        logger.info("测试Ollama组件...")
        
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
        
        logger.info("创建Ollama组件...")
        components = create_ollama_components(ollama_config)
        
        logger.info("测试思考模型LLM...")
        test_prompt = "1+1等于几？请只回答数字。"
        result = components['thinking_llm']._generate([test_prompt])
        logger.info(f"思考模型LLM测试结果: {result.generations[0][0].text}")
        
        logger.info("测试非思考模型LLM...")
        result = components['non_thinking_llm']._generate([test_prompt])
        logger.info(f"非思考模型LLM测试结果: {result.generations[0][0].text}")
        
        logger.info("测试Embeddings...")
        test_text = "这是一个测试文本"
        embedding = components['embeddings'].embed_query(test_text)
        logger.info(f"Embedding测试结果: 向量维度 {len(embedding)}")
        
        logger.info("所有组件测试通过！")
        return True
        
    except Exception as e:
        logger.error(f"组件测试失败: {e}")
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_components()
    if success:
        print("\n✅ 组件测试成功！")
        sys.exit(0)
    else:
        print("\n❌ 组件测试失败！")
        sys.exit(1)
