"""
Startup script for the Lumina FastAPI application.
This script ensures proper module resolution and starts the uvicorn server.
"""

from backend.main import app
import sys
import os
from pathlib import Path

# Add the project root to Python path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

# Import the FastAPI app from backend

if __name__ == "__main__":
    import uvicorn

    # Run the application
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,  # Enable auto-reload during development
        workers=1,
    )
