import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.ollama_client import OllamaClient
from app.config import OllamaConfig


def test_ollama_connection(config: OllamaConfig = None):
    if config is None:
        config = OllamaConfig()
    
    try:
        client = OllamaClient(
            model=config.model,
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
        
        return True
    except Exception as e:
        print(f"错误: {e}")
        print("\n请确保:")
        print("1. Ollama 服务已启动 (ollama serve)")
        print(f"2. 已下载 {config.model} 模型 (ollama pull {config.model})")
        return False


if __name__ == "__main__":
    test_ollama_connection()
