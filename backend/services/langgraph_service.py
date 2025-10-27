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


class LangGraphService:
    """
    Main service that orchestrates the LangGraph workflow.

    This service builds and compiles the complete workflow:
    START → evaluate_depth → retrieve_context → route → respond_* → END
    """

    def __init__(self):
        """Initialize the LangGraph workflow and compile it."""
        from langgraph.graph import StateGraph, START, END
        from .depth_evaluator import evaluate_depth
        from .lumina_responder import respond_shallow, respond_medium, respond_deep

        logger.info("Initializing LangGraph workflow...")

        # Create the state graph
        workflow = StateGraph(LuminaState)

        # Add nodes
        workflow.add_node("evaluate_depth", evaluate_depth)
        workflow.add_node("retrieve_context", retrieve_context)
        workflow.add_node("respond_shallow", respond_shallow)
        workflow.add_node("respond_medium", respond_medium)
        workflow.add_node("respond_deep", respond_deep)

        # Configure edges
        # START → evaluate_depth
        workflow.add_edge(START, "evaluate_depth")

        # evaluate_depth → retrieve_context
        workflow.add_edge("evaluate_depth", "retrieve_context")

        # retrieve_context → conditional routing based on depth
        workflow.add_conditional_edges(
            "retrieve_context",
            route_by_depth,
            {
                "shallow": "respond_shallow",
                "medium": "respond_medium",
                "deep": "respond_deep"
            }
        )

        # All response nodes → END
        workflow.add_edge("respond_shallow", END)
        workflow.add_edge("respond_medium", END)
        workflow.add_edge("respond_deep", END)

        # Compile the workflow
        self.app = workflow.compile()

        logger.info("LangGraph workflow compiled successfully")

    def process_checkin(self, user_input: str) -> dict:
        """
        Process a user check-in through the complete workflow.

        Args:
            user_input: The user's check-in text

        Returns:
            Dict with 'response' and 'depth' keys

        Raises:
            Exception: If workflow execution fails

        Logs:
            - INFO: Workflow start and completion with total time
        """
        start_time = time.time()

        logger.info(f"Workflow: Starting | Input: {user_input[:50]}...")

        # Create initial state
        initial_state: LuminaState = {
            "user_input": user_input,
            "depth_level": "medium",  # Will be overwritten by evaluate_depth
            "rag_contexts": [],
            "response": ""
        }

        try:
            # Invoke the workflow
            final_state = self.app.invoke(initial_state)

            elapsed = time.time() - start_time

            # Check if we exceeded timeout
            if elapsed > 10.0:
                logger.error(
                    f"Workflow: Timeout | Execution took {elapsed:.2f}s (>10s limit)")
                raise TimeoutError(
                    f"Workflow execution exceeded 10 seconds ({elapsed:.2f}s)")

            logger.info(
                f"Workflow: Complete | Depth: {final_state['depth_level']} | "
                f"Total time: {elapsed:.2f}s"
            )

            return {
                "response": final_state["response"],
                "depth": final_state["depth_level"]
            }

        except TimeoutError:
            raise
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(
                f"Workflow: Failed | Error: {e} | Time: {elapsed:.2f}s")
            raise
