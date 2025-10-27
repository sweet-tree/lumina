"""
Checkin endpoint for Lumina depth evaluation workflow.

This endpoint processes user check-ins through the LangGraph workflow
and returns Lumina's response based on the depth of self-inquiry.
"""

import logging
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

logger = logging.getLogger("lumina.api")

# Create router with /api prefix
router = APIRouter(prefix="/api", tags=["checkin"])


class CheckinRequest(BaseModel):
    """Request model for check-in endpoint."""
    user_input: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="User's check-in text (1-500 characters)"
    )


class CheckinResponse(BaseModel):
    """Response model for check-in endpoint."""
    response: str = Field(..., description="Lumina's response")
    depth: str = Field(...,
                       description="Depth classification: shallow, medium, or deep")


@router.post("/checkin", response_model=CheckinResponse)
async def process_checkin(request: CheckinRequest, req: Request):
    """
    Process a user check-in through the LangGraph workflow.

    This endpoint:
    1. Validates user input (1-500 characters)
    2. Processes through depth evaluation → RAG retrieval → response generation
    3. Returns Lumina's response and depth classification

    Args:
        request: CheckinRequest with user_input
        req: FastAPI Request object (to access app.state)

    Returns:
        CheckinResponse with response and depth

    Raises:
        HTTPException 400: Invalid input (handled by Pydantic)
        HTTPException 500: Workflow execution failed
        HTTPException 504: Workflow timeout (>10 seconds)
    """
    try:
        # Get LangGraphService from app state (initialized at startup)
        langgraph_service = req.app.state.langgraph_service

        logger.info(
            f"API: Checkin request | Input: {request.user_input[:50]}...")

        # Process through LangGraph workflow
        result = langgraph_service.process_checkin(request.user_input)

        logger.info(f"API: Checkin success | Depth: {result['depth']}")

        return CheckinResponse(
            response=result["response"],
            depth=result["depth"]
        )

    except TimeoutError as e:
        logger.error(f"API: Checkin timeout | Error: {e}")
        raise HTTPException(
            status_code=504,
            detail="Request timeout: Workflow execution exceeded 10 seconds"
        )

    except Exception as e:
        logger.error(f"API: Checkin failed | Error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error: Failed to process check-in"
        )
