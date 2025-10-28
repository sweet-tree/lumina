"""
Multi-Agent Depth System Service

Four-agent system for evaluating user check-ins:
1. Extraction Agent - Extract structured signal
2. Deep Agent - User model + memory + patterns
3. Teaching Agent - Pedagogical strategy
4. Card Agent - Reward logic
"""

import os
import logging
from pathlib import Path
from typing_extensions import TypedDict, Annotated
from operator import add
from dotenv import load_dotenv

from langgraph.store.postgres import PostgresStore
from langgraph.graph import StateGraph, START, END
from langgraph.store.base import BaseStore

# Load environment variables from backend/.env
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

logger = logging.getLogger("lumina.multi_agent")


# State Schema
class MultiAgentState(TypedDict):
    """State for multi-agent depth evaluation workflow"""

    # Input
    user_id: str
    user_input: str
    session_id: str

    # Extraction Agent output
    extraction: dict  # {body_signals, triggers, temporal, specificity_score}

    # Deep Agent output
    user_model: dict  # {baseline, patterns, trajectory, in_loop}
    relative_depth: str  # "shallow" | "medium" | "deep"

    # Teaching Agent output
    teaching_strategy: dict  # {strategy, guidance, reason}

    # Card Agent output
    card_decision: dict  # {award_card, card_id, rarity, reason}

    # Response generation
    rag_contexts: Annotated[list[dict], add]  # Spiritual wisdom
    final_response: str


class MultiAgentService:
    """Service for multi-agent depth evaluation system"""

    def __init__(self):
        """Initialize PostgresStore and workflow"""
        self.db_uri = os.getenv("DATABASE_URL")
        if not self.db_uri:
            raise ValueError("DATABASE_URL not found in environment variables")

        # Initialize PostgresStore context manager and enter it
        self._store_cm = PostgresStore.from_conn_string(self.db_uri)
        self.store = self._store_cm.__enter__()
        logger.info("PostgresStore initialized")

        # Build workflow (agents will be added in later tasks)
        self.workflow = self._build_workflow()

    def setup_store(self):
        """
        Run once to create Store tables in Supabase.
        Call this during initial setup or deployment.
        """
        try:
            self.store.setup()
            logger.info("PostgresStore tables created successfully")
        except Exception as e:
            logger.error(f"Failed to setup PostgresStore: {e}")
            raise

    def _build_workflow(self) -> StateGraph:
        """Build LangGraph workflow with agents"""
        builder = StateGraph(MultiAgentState)

        # TODO: Add agent nodes in subsequent tasks
        # builder.add_node("extraction", extraction_agent)
        # builder.add_node("deep", deep_agent)
        # builder.add_node("teaching", teaching_agent)
        # builder.add_node("card", card_agent)
        # builder.add_node("response", generate_response)

        # TODO: Add edges
        # builder.add_edge(START, "extraction")
        # builder.add_edge("extraction", "deep")
        # ...

        logger.info("Workflow structure initialized (agents to be added)")
        return builder

    def process_checkin(self, user_id: str, user_input: str, session_id: str = None) -> dict:
        """
        Process a user check-in through the multi-agent system.

        Args:
            user_id: User identifier
            user_input: User's check-in text
            session_id: Optional session identifier

        Returns:
            dict with response, card_decision, and depth
        """
        # TODO: Implement in later tasks once agents are built
        logger.info(f"Processing check-in for user {user_id}")

        # Placeholder response
        return {
            "response": "Multi-agent system not yet implemented",
            "card_decision": {"award_card": False},
            "depth": "medium"
        }

    def close(self):
        """Close Store connection"""
        if hasattr(self, '_store_cm'):
            self._store_cm.__exit__(None, None, None)


# Singleton instance
_service_instance = None


def get_multi_agent_service() -> MultiAgentService:
    """Get or create MultiAgentService singleton"""
    global _service_instance
    if _service_instance is None:
        _service_instance = MultiAgentService()
    return _service_instance
