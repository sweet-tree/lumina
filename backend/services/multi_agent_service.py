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

# Import agent node functions
from .extraction_agent import extraction_agent_node
from .deep_agent import deep_agent_node
from .teaching_agent import teaching_agent_node
from .card_agent import card_agent_node
from .response_generation import response_generation_node

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
        """Initialize service with database URI and Store"""
        self.db_uri = os.getenv("DATABASE_URL")
        if not self.db_uri:
            raise ValueError("DATABASE_URL not found in environment variables")

        # Create Store context manager and enter it (keep alive for service lifetime)
        self._store_cm = PostgresStore.from_conn_string(self.db_uri)
        self.store = self._store_cm.__enter__()

        # Build and compile workflow once (reuse for all requests)
        self.graph = self._build_workflow(self.store)

        logger.info(
            "MultiAgentService initialized with persistent Store and compiled graph")

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

    def _build_workflow(self, store: BaseStore):
        """Build and compile LangGraph workflow with all agents"""
        builder = StateGraph(MultiAgentState)

        # Add agent nodes
        builder.add_node("extraction", extraction_agent_node)
        builder.add_node(
            "deep", lambda state: deep_agent_node(state, store=store))
        builder.add_node("teaching", teaching_agent_node)
        builder.add_node("card", card_agent_node)
        builder.add_node("response", response_generation_node)

        # Configure edges
        # Sequential: START → Extraction → Deep Agent
        builder.add_edge(START, "extraction")
        builder.add_edge("extraction", "deep")

        # Parallel: Deep Agent → (Teaching Agent + Card Agent)
        builder.add_edge("deep", "teaching")
        builder.add_edge("deep", "card")

        # Convergence: (Teaching + Card) → Response Generation
        builder.add_edge("teaching", "response")
        builder.add_edge("card", "response")

        # End: Response Generation → END
        builder.add_edge("response", END)

        logger.info(
            "Workflow built: extraction → deep → (teaching + card) → response")
        return builder.compile()

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
        import time
        start_time = time.time()

        logger.info(
            f"Processing check-in for user {user_id}: {user_input[:50]}...")

        # Prepare initial state
        initial_state = {
            "user_id": user_id,
            "user_input": user_input,
            "session_id": session_id or f"session_{int(time.time())}"
        }

        # Run workflow (graph and store are persistent, reused across requests)
        try:
            final_state = self.graph.invoke(initial_state)

            elapsed = time.time() - start_time
            logger.info(f"Check-in processed in {elapsed:.2f}s")

            # Extract results
            return {
                "response": final_state.get("final_response", ""),
                "card_decision": final_state.get("card_decision", {"award_card": False}),
                "depth": final_state.get("relative_depth", "medium"),
                "teaching_strategy": final_state.get("teaching_strategy", {}),
                "extraction": final_state.get("extraction", {})
            }

        except Exception as e:
            logger.error(f"Error processing check-in: {e}", exc_info=True)
            # Return fallback response
            return {
                "response": "What's here right now?",
                "card_decision": {"award_card": False, "reason": "Error in processing"},
                "depth": "medium",
                "error": str(e)
            }

    def close(self):
        """Close Store connection (call on application shutdown)"""
        if hasattr(self, '_store_cm'):
            self._store_cm.__exit__(None, None, None)
            logger.info("Store connection closed")


# Singleton instance
_service_instance = None


def get_multi_agent_service() -> MultiAgentService:
    """Get or create MultiAgentService singleton"""
    global _service_instance
    if _service_instance is None:
        _service_instance = MultiAgentService()
    return _service_instance
