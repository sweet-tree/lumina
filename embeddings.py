from openai import OpenAI
from typing import List
from backend.config import Config


class EmbeddingService:
    """Service for generating embeddings with Qwen3-Embedding-8B on Nebius."""

    def __init__(self):
        Config.validate()
        self.api_key = Config.NEBIUS_API_KEY
        self.base_url = Config.NEBIUS_BASE_URL
        self.model = Config.QWEN_EMBEDDING_MODEL
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )

    def create_embedding(self, text: str) -> List[float]:
        """
        Generate an embedding for a given text.

        Args:
            text: Input text to embed

        Returns:
            List of embedding values

        Raises:
            Exception: If the API request fails or the response is invalid
        """
        response = self.client.embeddings.create(
            model=self.model,
            input=text
        )

        return response.data[0].embedding

    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.

        Args:
            texts: List of input texts to embed

        Returns:
            List of embedding vectors
        """
        response = self.client.embeddings.create(
            model=self.model,
            input=texts
        )

        return [item.embedding for item in response.data]
