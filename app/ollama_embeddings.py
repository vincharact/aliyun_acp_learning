from typing import List
from langchain_core.embeddings import Embeddings
from utils.ollama_client import OllamaClient


class OllamaEmbeddings(Embeddings):
    def __init__(self, client: OllamaClient):
        self.client = client

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings = []
        for text in texts:
            response = self.client.client.embeddings(model=self.client.model, prompt=text)
            embeddings.append(response["embedding"])
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        response = self.client.client.embeddings(model=self.client.model, prompt=text)
        return response["embedding"]
