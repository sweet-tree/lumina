from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from typing import List
from backend.config import Config


class ChatService:
    """Service for handling chat completions with Qwen models on Nebius."""

    def __init__(self):
        Config.validate()
        self.api_key = Config.NEBIUS_API_KEY
        self.base_url = Config.NEBIUS_BASE_URL
        self.model = Config.QWEN_CHAT_MODEL
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )

    def generate(self, prompt: str, max_tokens: int = 1024, temperature: float = 0.7) -> str:
        """
        Generate a completion for a given prompt.

        Args:
            prompt: Input text for the model
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature

        Returns:
            Generated text response
        """
        messages: List[ChatCompletionMessageParam] = [
            {"role": "user", "content": prompt}  # type: ignore
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )

        if response.choices[0].message.content is None:
            return ""
        return response.choices[0].message.content

    def chat(self, messages: List[ChatCompletionMessageParam], max_tokens: int = 1024, temperature: float = 0.7) -> str:
        """
        Generate a completion for a chat conversation.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature

        Returns:
            Generated text response
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )

        if response.choices[0].message.content is None:
            return ""
        return response.choices[0].message.content
