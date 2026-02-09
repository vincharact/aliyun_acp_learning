from typing import Any, Dict

from ollama_client import OllamaClient

from config import OllamaConfig
from logger import logger
from ollama_embeddings import OllamaEmbeddings
from ragas_ollama_wrapper import OllamaLLM


def _create_client(config: OllamaConfig, model: str) -> OllamaClient:
    return OllamaClient(
        model=model,
        base_url=config.base_url,
        timeout=config.timeout
    )


def create_ollama_components(config: OllamaConfig = None) -> Dict[str, Any]:
    if config is None:
        config = OllamaConfig()
    
    logger.info("创建Ollama组件...")
    
    thinking_client = _create_client(config, config.non_thinking_model)
    non_thinking_client = _create_client(config, config.non_thinking_model)
    embedding_client = _create_client(config, config.embedding_model)
    rerank_client = _create_client(config, config.rerank_model)
    
    thinking_llm = OllamaLLM(
        client=thinking_client,
        temperature=config.temperature,
        top_p=config.top_p
    )
    
    non_thinking_llm = OllamaLLM(
        client=non_thinking_client,
        temperature=config.temperature,
        top_p=config.top_p
    )
    
    embeddings = OllamaEmbeddings(client=embedding_client)
    
    logger.info("Ollama组件创建完成")
    
    return {
        'thinking_client': thinking_client,
        'non_thinking_client': non_thinking_client,
        'embedding_client': embedding_client,
        'rerank_client': rerank_client,
        'thinking_llm': thinking_llm,
        'non_thinking_llm': non_thinking_llm,
        'embeddings': embeddings
    }


def create_evaluation_components(config: OllamaConfig = None):
    if config is None:
        config = OllamaConfig()
    
    logger.info("创建评估组件...")
    
    llm_client = _create_client(config, config.non_thinking_model)
    embedding_client = _create_client(config, config.embedding_model)
    
    llm = OllamaLLM(
        client=llm_client,
        temperature=config.temperature,
        top_p=config.top_p
    )
    
    embeddings = OllamaEmbeddings(client=embedding_client)
    
    logger.info("评估组件创建完成")
    
    return llm_client, llm, embeddings
