from typing import List

from langchain_core.embeddings import Embeddings

from ollama_client import OllamaClient

from logger import logger


class OllamaEmbeddings(Embeddings):
    def __init__(self, client: OllamaClient):
        self.client = client

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            logger.warning("embed_documents called with empty list")
            return []
        
        try:
            embeddings = []
            for text in texts:
                response = self.client.client.embeddings(model=self.client.model, prompt=text)
                embeddings.append(response["embedding"])
            logger.debug(f"文档嵌入完成，处理了 {len(texts)} 个文本")
            return embeddings
        except Exception as e:
            logger.error(f"文档嵌入失败: {e}")
            raise

    def embed_query(self, text: str) -> List[float]:
        if not text:
            logger.warning("embed_query called with empty string")
            return []
        
        try:
            response = self.client.client.embeddings(model=self.client.model, prompt=text)
            logger.debug("查询嵌入完成")
            return response["embedding"]
        except Exception as e:
            logger.error(f"查询嵌入失败: {e}")
            raise
