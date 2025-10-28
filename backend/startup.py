"""
Application Startup and Shutdown Handlers

Initializes and cleans up the Multi-Agent Service.
"""

import logging
from .services.multi_agent_service import get_multi_agent_service

logger = logging.getLogger("lumina.startup")


def startup_handler():
    """
    Initialize services on application startup.

    This creates the MultiAgentService singleton which:
    - Connects to PostgresStore
    - Compiles the LangGraph workflow
    - Keeps both alive for the application lifetime
    """
    try:
        logger.info("Initializing Multi-Agent Service...")
        service = get_multi_agent_service()
        logger.info("✓ Multi-Agent Service initialized successfully")
        logger.info("  - PostgresStore connected")
        logger.info("  - LangGraph workflow compiled")
        logger.info("  - Ready to process check-ins")
    except Exception as e:
        logger.error(
            f"Failed to initialize Multi-Agent Service: {e}", exc_info=True)
        raise


def shutdown_handler():
    """
    Clean up services on application shutdown.

    This closes the PostgresStore connection gracefully.
    """
    try:
        logger.info("Shutting down Multi-Agent Service...")
        service = get_multi_agent_service()
        service.close()
        logger.info("✓ Multi-Agent Service shut down successfully")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}", exc_info=True)
