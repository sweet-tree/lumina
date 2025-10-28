"""
User Memory Helper Functions

High-level abstraction layer for LangGraph PostgresStore operations.
Provides clean interface for reading/writing user memory data.
"""

import logging
from typing import Optional
from langgraph.store.base import BaseStore

logger = logging.getLogger("lumina.user_memory")


def get_user_baseline(store: BaseStore, user_id: str) -> float:
    """
    Get user's baseline specificity score.

    Args:
        store: LangGraph Store instance
        user_id: User identifier

    Returns:
        float: Baseline specificity score (default 5.0 for new users)
    """
    namespace = ("memories", user_id)
    item = store.get(namespace, "baseline")

    if item and item.value:
        return item.value.get("current_baseline", 5.0)

    logger.info(f"No baseline found for user {user_id}, using default 5.0")
    return 5.0


def update_user_baseline(store: BaseStore, user_id: str, new_score: float) -> None:
    """
    Update user's baseline with rolling average of last 20 scores.

    Args:
        store: LangGraph Store instance
        user_id: User identifier
        new_score: New specificity score to add
    """
    namespace = ("memories", user_id)
    current = store.get(namespace, "baseline")

    if current and current.value:
        data = current.value
        scores = data.get("last_20_scores", [])
        scores.append(new_score)
        scores = scores[-20:]  # Keep only last 20

        baseline = sum(scores) / len(scores)

        store.put(namespace, "baseline", {
            "current_baseline": baseline,
            "checkin_count": data.get("checkin_count", 0) + 1,
            "last_20_scores": scores
        })

        logger.info(f"Updated baseline for user {user_id}: {baseline:.2f}")
    else:
        # First check-in
        store.put(namespace, "baseline", {
            "current_baseline": new_score,
            "checkin_count": 1,
            "last_20_scores": [new_score]
        })

        logger.info(f"Created baseline for user {user_id}: {new_score}")


def get_user_patterns(store: BaseStore, user_id: str) -> dict:
    """
    Get detected loops, doorways, and triggers for user.

    Args:
        store: LangGraph Store instance
        user_id: User identifier

    Returns:
        dict: {loops: [...], doorways: [...]}
    """
    namespace = ("memories", user_id)
    item = store.get(namespace, "loops_doorways")

    if item and item.value:
        return item.value

    logger.info(f"No patterns found for user {user_id}")
    return {"loops": [], "doorways": []}


def update_body_patterns(store: BaseStore, user_id: str, body_signals: list) -> None:
    """
    Update body pattern frequencies.

    Args:
        store: LangGraph Store instance
        user_id: User identifier
        body_signals: List of "location: sensation" strings
    """
    namespace = ("memories", user_id)
    current = store.get(namespace, "body_patterns")
    patterns = current.value if (current and current.value) else {}

    for signal in body_signals:
        # Extract location from "location: sensation" format
        if ":" in signal:
            location = signal.split(":")[0].strip()
            patterns[location] = patterns.get(location, 0) + 1

    store.put(namespace, "body_patterns", patterns)
    logger.info(f"Updated body patterns for user {user_id}: {patterns}")


def update_triggers(store: BaseStore, user_id: str, triggers: list) -> None:
    """
    Update trigger frequencies.

    Args:
        store: LangGraph Store instance
        user_id: User identifier
        triggers: List of trigger strings (e.g., ["meeting", "monday"])
    """
    namespace = ("memories", user_id)
    current = store.get(namespace, "triggers")
    trigger_counts = current.value if (current and current.value) else {}

    for trigger in triggers:
        trigger_counts[trigger] = trigger_counts.get(trigger, 0) + 1

    store.put(namespace, "triggers", trigger_counts)
    logger.info(f"Updated triggers for user {user_id}: {trigger_counts}")


def get_body_patterns(store: BaseStore, user_id: str) -> dict:
    """
    Get body pattern frequencies for user.

    Args:
        store: LangGraph Store instance
        user_id: User identifier

    Returns:
        dict: {location: count, ...}
    """
    namespace = ("memories", user_id)
    item = store.get(namespace, "body_patterns")

    if item and item.value:
        return item.value

    return {}


def get_triggers(store: BaseStore, user_id: str) -> dict:
    """
    Get trigger frequencies for user.

    Args:
        store: LangGraph Store instance
        user_id: User identifier

    Returns:
        dict: {trigger: count, ...}
    """
    namespace = ("memories", user_id)
    item = store.get(namespace, "triggers")

    if item and item.value:
        return item.value

    return {}


def get_recent_scores(store: BaseStore, user_id: str, limit: int = 5) -> list:
    """
    Get recent specificity scores for trajectory calculation.

    Args:
        store: LangGraph Store instance
        user_id: User identifier
        limit: Number of recent scores to return

    Returns:
        list: Recent specificity scores (most recent last)
    """
    namespace = ("memories", user_id)
    item = store.get(namespace, "baseline")

    if item and item.value:
        scores = item.value.get("last_20_scores", [])
        return scores[-limit:] if len(scores) > limit else scores

    return []
