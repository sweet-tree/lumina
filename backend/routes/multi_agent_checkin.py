"""
Multi-Agent Check-in Endpoint

New endpoint using the Multi-Agent Depth System.
Does not modify existing checkin.py - this is a separate implementation.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import logging

from ..services.multi_agent_service import get_multi_agent_service, MultiAgentService
from ..middleware.auth import get_current_user

logger = logging.getLogger("lumina.multi_agent_checkin")

router = APIRouter(prefix="/api/v2", tags=["multi-agent"])


class CheckinRequest(BaseModel):
    """Request model for multi-agent check-in"""
    user_input: str
    session_id: Optional[str] = None


class CheckinResponse(BaseModel):
    """Response model for multi-agent check-in"""
    response: str
    depth: str
    card_decision: dict
    teaching_strategy: dict
    extraction: dict


@router.post("/checkin", response_model=CheckinResponse)
async def multi_agent_checkin(
    request: CheckinRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Process check-in using Multi-Agent Depth System.

    This is the new v2 endpoint that uses:
    - Extraction Agent (signal extraction)
    - Deep Agent (memory + patterns)
    - Teaching Agent (pedagogical strategy)
    - Card Agent (reward logic)
    - Response Generation (RAG + Plant Teacher voice)

    Args:
        request: CheckinRequest with user_input and optional session_id
        current_user: Authenticated user from JWT token

    Returns:
        CheckinResponse with response, depth, card decision, etc.
    """
    try:
        user_id = current_user["user_id"]

        logger.info(
            f"Multi-agent check-in for user {user_id}: {request.user_input[:50]}...")

        # Get service singleton
        service = get_multi_agent_service()

        # Process check-in through multi-agent workflow
        result = service.process_checkin(
            user_id=user_id,
            user_input=request.user_input,
            session_id=request.session_id
        )

        # Check for errors
        if "error" in result:
            logger.error(f"Multi-agent workflow error: {result['error']}")
            # Return fallback response but don't fail the request
            # The workflow already returned a fallback response

        return CheckinResponse(
            response=result["response"],
            depth=result["depth"],
            card_decision=result["card_decision"],
            teaching_strategy=result.get("teaching_strategy", {}),
            extraction=result.get("extraction", {})
        )

    except Exception as e:
        logger.error(f"Error in multi-agent check-in: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to process check-in"
        )


@router.get("/health")
async def health_check():
    """
    Health check endpoint for multi-agent system.

    Returns:
        Status of the multi-agent service
    """
    try:
        service = get_multi_agent_service()
        return {
            "status": "healthy",
            "service": "multi-agent-depth-system",
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=503,
            detail="Multi-agent service unavailable"
        )
