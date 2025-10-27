"""
LangGraph service for Lumina depth evaluation workflow.

This service orchestrates the multi-agent workflow that:
1. Evaluates user check-in depth (shallow/medium/deep)
2. Retrieves relevant spiritual wisdom via RAG
3. Generates contextually appropriate responses from Lumina
"""

import logging
import time
from typing import Literal
from typing_extensions import TypedDict, Annotated
from operator import add
from .vector_store_service import VectorStore


class LuminaState(TypedDict):
    """
    State object that flows through the LangGraph workflow.

    Fields:
        user_input: The user's check-in text ("What's here right now?")
        depth_level: Classification result - "shallow", "medium", or "deep"
        rag_contexts: List of retrieved spiritual wisdom from various sources.
                     Each dict contains {"source": str, "passages": list[str]}.
                     Uses reducer to support future parallel retrieval from
                     multiple sources (Buddhist, Vedic, shamanic).
        response: Final Lumina response to the user
    """
    user_input: str
    depth_level: Literal["shallow", "medium", "deep"]
    rag_contexts: Annotated[list[dict], add]
    response: str


logger = logging.getLogger("lumina.langgraph")


def retrieve_context(state: LuminaState) -> dict:
    """
    Retrieves relevant spiritual wisdom from vector store.

    This function searches the spiritual-library namespace in Pinecone
    for passages relevant to the user's check-in. Results are structured
    to support future parallel retrieval from multiple sources.

    Args:
        state: Current workflow state with user_input

    Returns:
        Dict with rag_contexts key containing list of retrieved passages

    Logs:
        - INFO: Query text (truncated) and number of passages retrieved
        - ERROR: Vector store failures (continues with empty contexts)
    """
    start_time = time.time()
    user_input = state["user_input"]

    logger.info(f"Node: retrieve_context | Query: {user_input[:50]}...")

    try:
        # Initialize vector store
        vector_store = VectorStore()

        # Search spiritual-library namespace
        # VectorStore.search returns top 3 reranked results by default
        results = vector_store.search(
            query=user_input,
            top_k=10,  # Retrieve 10 candidates for reranking
            namespace="spiritual-library"
        )

        # Extract passages from results
        passages = [result["text"] for result in results]

        # Structure as dict with source and passages
        # Ready for future parallel retrieval from multiple sources
        rag_contexts = [{
            "source": "spiritual-library",
            "passages": passages
        }]

        elapsed = time.time() - start_time
        logger.info(
            f"Node: retrieve_context | Retrieved: {len(passages)} passages | "
            f"Time: {elapsed:.2f}s"
        )

        return {"rag_contexts": rag_contexts}

    except Exception as e:
        # Log error but continue workflow with empty contexts
        elapsed = time.time() - start_time
        logger.error(
            f"Node: retrieve_context | Error: {e} | Time: {elapsed:.2f}s"
        )
        logger.warning(
            "Node: retrieve_context | Continuing with empty rag_contexts")

        return {"rag_contexts": []}


def route_by_depth(state: LuminaState) -> Literal["shallow", "medium", "deep"]:
    """
    Routes workflow to appropriate response node based on depth classification.

    This function is used by LangGraph's conditional edges to determine
    which response generator to invoke based on the depth_level in state.

    Args:
        state: Current workflow state with depth_level

    Returns:
        Node name to route to: "shallow", "medium", or "deep"

    Logs:
        - INFO: Routing decision (depth level)
    """
    depth = state["depth_level"]
    logger.info(f"Routing: depth={depth} → respond_{depth}")
    return depth
