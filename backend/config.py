import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from backend/.env
backend_dir = Path(__file__).parent
env_path = backend_dir / ".env"
load_dotenv(env_path)


class Config:
    # API Configuration
    NEBIUS_API_KEY = os.getenv("NEBIUS_API_KEY")
    NEBIUS_BASE_URL = os.getenv(
        "NEBIUS_BASE_URL", "https://api.studio.nebius.com/v1/")

    # Model Configuration
    QWEN_CHAT_MODEL = os.getenv(
        "QWEN_CHAT_MODEL", "Qwen/Qwen3-Coder-30B-A3B-Instruct")
    QWEN_EMBEDDING_MODEL = os.getenv(
        "QWEN_EMBEDDING_MODEL", "Qwen/Qwen3-Embedding-8B")

    # API Keys
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

    # Validation
    @classmethod
    def validate(cls):
        if not cls.NEBIUS_API_KEY:
            raise ValueError("NEBIUS_API_KEY environment variable is required")
        if not cls.PINECONE_API_KEY:
            raise ValueError(
                "PINECONE_API_KEY environment variable is required")
