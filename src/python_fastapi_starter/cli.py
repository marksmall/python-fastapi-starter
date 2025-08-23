"""
CLI utilities and entry points for the FastAPI project. Includes server
startup, test, lint, format, release, and postinstall commands.
"""

import os
import shutil
import socket
import subprocess  # noqa: S404
import sys

import uvicorn
from dsp_toolkit.cli import lint_and_format as dsp_lint_and_format
from dsp_toolkit.cli import release as dsp_release
from dsp_toolkit.cli import test as dsp_test
from dsp_toolkit.env import load_environment
from dsp_toolkit.logging_config import logger


def find_free_port(start_port: int = 8000):
    """
    Find an available port starting from start_port.
    Returns the first free port found in the range.
    """
    for port in range(start_port, start_port + 100):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("localhost", port))
                return port
        except OSError:
            continue
    raise RuntimeError("No free ports found")


def main():
    """
    Main entry point for development server.
    Loads environment, finds free port, and starts FastAPI app with Uvicorn.
    """
    logger.info("Development mode activated")

    load_environment()

    logger.info("Loaded environment variables using load_environment() helper.")
    logger.debug("ROOT_PATH set to: %s", os.getenv("ROOT_PATH"))
    port = find_free_port()
    logger.info("Starting server on port %d", port)
    uvicorn.run("python_fastapi_starter.api.main:app", host="127.0.0.1", port=port, reload=True)


def test():
    """
    Run tests using pytest. Accepts additional arguments.
    """
    logger.info("Running tests.")
    sys.exit(dsp_test())


def lint_and_format():
    """
    Run Ruff to format code and fix lint issues (including import sorting).
    Accepts additional arguments (e.g., directories or files).
    """
    logger.info("Running lint and format.")
    sys.exit(dsp_lint_and_format())


def release():
    """
    Run semantic-release to publish a new release.
    """
    logger.info("Running release.")
    sys.exit(dsp_release())


def postinstall():
    """
    Run postinstall.sh script for project setup tasks.
    """
    logger.info("Running postinstall script.")
    # S404: subprocess usage is documented and input is trusted (static script name)
    # S607: Use full path to 'sh' executable
    # S603: No untrusted input is passed to subprocess
    sh_path = shutil.which("sh")
    if not sh_path:
        logger.error("Could not find 'sh' executable in PATH.")
        sys.exit(1)
    sys.exit(subprocess.call([sh_path, "postinstall.sh"]))  # noqa:603


if __name__ == "__main__":
    main()
