import sys

from ollama_client import OllamaClient

from config import OllamaConfig
from logger import logger


def test_ollama_connection(config: OllamaConfig = None):
    if config is None:
        config = OllamaConfig()
    
    try:
        logger.info("测试Ollama连接...")
        
        client = OllamaClient(
            model=config.non_thinking_model,
            base_url=config.base_url,
            timeout=config.timeout
        )
        
        models_response = client.list_models()
        print("可用的模型:")
        if models_response:
            for model in models_response:
                print(f"  - {model}")
        else:
            print("  (没有找到模型)")
        
        print("\n测试简单对话:")
        messages = [
            {"role": "user", "content": "你好，请用一句话介绍你自己。"}
        ]
        response = client.chat(messages)
        print(f"回复: {response['message']['content']}")
        
        logger.info("Ollama连接测试成功！")
        return True
    except Exception as e:
        logger.error(f"Ollama连接测试失败: {e}")
        print(f"错误: {e}")
        print("\n请确保:")
        print("1. Ollama 服务已启动 (ollama serve)")
        print(f"2. 已下载 {config.non_thinking_model} 模型 (ollama pull {config.non_thinking_model})")
        return False


if __name__ == "__main__":
    success = test_ollama_connection()
    if success:
        print("\n✅ Ollama连接测试成功！")
        sys.exit(0)
    else:
        print("\n❌ Ollama连接测试失败！")
        sys.exit(1)
