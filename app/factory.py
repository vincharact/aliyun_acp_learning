from utils.ollama_client import OllamaClient
from app.ragas_ollama_wrapper import OllamaLLM
from app.ollama_embeddings import OllamaEmbeddings
from app.config import OllamaConfig


def create_ollama_components(config: OllamaConfig = None):
    if config is None:
        config = OllamaConfig()
    
    ollama_client = OllamaClient(
        model=config.model,
        base_url=config.base_url,
        timeout=config.timeout
    )
    
    llm = OllamaLLM(
        client=ollama_client,
        temperature=config.temperature,
        top_p=config.top_p
    )
    
    embeddings = OllamaEmbeddings(client=ollama_client)
    
    return ollama_client, llm, embeddings
