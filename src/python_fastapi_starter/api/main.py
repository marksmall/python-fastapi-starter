"""
Main FastAPI application for the starter project.
Defines the API endpoints and app instance.
"""

from .app import create_app

app = create_app()


@app.get("/")
def read_root():
    """
    Root endpoint for health check and welcome message.
    Returns a JSON response with a greeting.
    """
    return {"message": "Hello, FastAPI starter!"}
