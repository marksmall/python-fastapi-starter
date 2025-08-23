"""
Test suite for the FastAPI starter project.

Includes tests for the root endpoint.
"""

from fastapi.testclient import TestClient

from python_fastapi_starter.api.main import app


def test_read_root():
    """
    Test the root endpoint ('/') of the FastAPI app.

    Verifies status code and response payload.
    """
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI starter!"}
