"""
LangGraph service for Lumina depth evaluation workflow.

This service orchestrates the multi-agent workflow that:
1. Evaluates user check-in depth (shallow/medium/deep)
2. Retrieves relevant spiritual wisdom via RAG
3. Generates contextually appropriate responses from Lumina
"""

from typing import Literal
from typing_extensions import TypedDict, Annotated
from operator import add


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
