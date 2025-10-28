from backend.services.rag_service import RAGService
from backend.services.langgraph_service import LangGraphService
from backend.routes import checkin
from backend.routes import multi_agent_checkin
from backend.startup import startup_handler, shutdown_handler
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create FastAPI application instance
app = FastAPI(
    title="Lumina API",
    description="Backend API for the Lumina document processing system",
    version="0.1.0"
)

# Initialize LangGraph service at startup (singleton)
# This compiles the workflow once and reuses it for all requests
app.state.langgraph_service = LangGraphService()

# Add startup and shutdown handlers for Multi-Agent Service
app.add_event_handler("startup", startup_handler)
app.add_event_handler("shutdown", shutdown_handler)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(checkin.router)  # Existing v1 endpoint
app.include_router(multi_agent_checkin.router)  # New v2 multi-agent endpoint

# Request model for chat endpoint


class ChatRequest(BaseModel):
    message: str

# Response model for chat endpoint


class ChatResponse(BaseModel):
    success: bool
    response: Optional[str] = None
    error: Optional[str] = None

# Health check endpoint


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {
        "status": "healthy",
        "message": "FastAPI server is running",
        "version": app.version
    }

# Root endpoint


@app.get("/")
async def root():
    """
    Root endpoint providing basic API information.
    """
    return {
        "message": "Welcome to Lumina API",
        "documentation": "/docs",
        "health": "/health"
    }


# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Chat endpoint to process user messages and return AI responses using RAG.
    """
    try:
        # Initialize RAG service
        rag_service = RAGService()

        # Generate response using RAG service
        response = rag_service.generate_response(request.message)

        return ChatResponse(
            success=True,
            response=response
        )
    except Exception as e:
        return ChatResponse(
            success=False,
            error=str(e)
        )
