"""
App factory for FastAPI project.
Sets up the FastAPI instance, middleware, and configuration.
"""

import logging
import os

from dsp_toolkit.env import load_environment
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_environment()

ROOT_PATH = os.getenv("ROOT_PATH", "")


def create_app() -> FastAPI:
    """
    Create and configure a FastAPI application instance.
    Adds CORS middleware and any other global configuration.

    Returns:
        FastAPI: Configured FastAPI app instance.
    """
    app = FastAPI(
        title="Water Quality Archive",
        root_path=ROOT_PATH,
        openapi_tags=[],
        redoc_url="/redoc",
        version="0.9.1",
        logger=logging.getLogger("uvicorn.error"),
    )

    # Allow all origins (open API)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
