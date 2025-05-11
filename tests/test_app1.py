import pytest
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient
import pytest_asyncio
from pathlib import Path
from balanced_instance.app1 import app
from balanced_instance.app1 import STATIC_DIR

"""
This test suite validates the core functionality of the FastAPI application:
- It performs asynchronous tests on the root HTML endpoint and a PDF file endpoint to verify content type,
  status codes, and content correctness.
- It uses a parametrized synchronous test to check a number divisor counting endpoint for multiple cases.
- Both asynchronous and synchronous test clients are used to simulate HTTP requests internally without external network calls.
- The tests ensure correctness, content integrity, and expected application behavior through response validation.
"""

# Define an asynchronous fixture providing an AsyncClient instance connected to the FastAPI app
@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
        # ASGITransport allows AsyncClient to interact with ASGI apps without actual HTTP
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client

# Create a synchronous test client instance for simple tests (not async)
client = TestClient(app)

# Asynchronous test: Verify that the root endpoint ("/") returns valid HTML content
@pytest.mark.asyncio
async def test_read_root(async_client):
    """Test root endpoint returns valid HTML response"""
    response = await async_client.get("/")
    
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    
    html_file = STATIC_DIR / "hello_w.html"
    expected_content = html_file.read_text()
    
    normalized_response = ' '.join(response.text.split())
    normalized_expected = ' '.join(expected_content.split())
    
    assert normalized_response == normalized_expected
    assert "Hi, girl" in response.text

# Asynchronous test: Check that the /media_example endpoint returns a valid PDF file
@pytest.mark.asyncio
async def test_media_example(async_client):
    """Test PDF endpoint returns correct file"""
    response = await async_client.get("/media_example")
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert len(response.content) > 0
    assert response.content[:4] == b'%PDF'

# Parametrized synchronous test: Validate a number divisor-counting endpoint for various cases
@pytest.mark.parametrize("input_num,expected", [
    (1, 1), (2, 2), (5, 2), (6, 4), (13, 2), (24, 8)
])
def test_add_numbers(input_num, expected):
    """Test number divisor counting function"""
    response = client.get(f"/prime/{input_num}")
    assert response.status_code == 200
    assert response.json()["result"] == expected