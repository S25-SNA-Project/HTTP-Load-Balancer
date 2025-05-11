import argparse
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
import httpx

"""
This test suite covers the core proxying and task management behavior of the FastAPI app2 instance
within a load-balanced system. It uses FastAPI's TestClient for synchronous testing, pytest fixtures 
for setup/cleanup, and monkeypatching/mocking to isolate external dependencies (like HTTP requests 
and logging). It verifies the correct response behavior for task registration, access control, 
proxy redirection, and proxy forwarding for registered clients.
"""

# Dummy asynchronous HTTP client to mock external HTTP calls made via httpx.AsyncClient
class DummyAsyncClient:
    def __init__(self, *args, **kwargs):
        pass
    async def __aenter__(self):
        return self
    async def __aexit__(self, *args):
        pass
    async def request(self, *args, **kwargs):
        return self._resp
    async def post(self, *args, **kwargs):
        return MagicMock(status_code=200)


# Fixture that automatically patches command-line arguments and some module-level dependencies in app2
@pytest.fixture(autouse=True)
def patch_args_and_import(mocker):
    mocker.patch(
        "argparse.ArgumentParser.parse_known_args",
        return_value=(
            argparse.Namespace(
                config_file="tests/test_config.json",
                application_port=8888,
                balanced_port=8080,
                balancer_addr="testclient:8000"
            ),
            []
        )
    )
    # Import app2 after patching so it reads mocked args
    from balanced_instance import app2
    # Mock internal logger and lock to avoid real threading and logging
    mocker.patch.object(app2, "logger", MagicMock())
    mocker.patch.object(app2, "lock", MagicMock())
    return app2

# Fixture for creating a TestClient and resetting application state before and after each test
@pytest.fixture
def client(patch_args_and_import):
    app2 = patch_args_and_import
    client = TestClient(app2.app)
    yield client, app2
    app2.active_waiting_clients.clear()
    app2.active_tasks = 0
    app2.BALANCER_ADDR = "testclient:8000"


# Test: /tasks_count endpoint should register client IP and return active tasks count
def test_tasks_count_balancer_only(client):
    client, app2 = client
    response = client.post(
        "/tasks_count",
        json={"client_ip": "1.2.3.4"}
    )
    assert response.status_code == 200
    assert response.json() == {"active_tasks": 0}
    assert "1.2.3.4" in app2.active_waiting_clients

# Test: /tasks_count should reject requests if balancer address doesn't match authorized address
def test_tasks_count_forbidden(client, monkeypatch):
    client, app2 = client
    monkeypatch.setattr(app2, "BALANCER_ADDR", "otherhost:1234")
    response = client.post("/tasks_count", json={"client_ip": "5.6.7.8"})
    assert response.status_code == 403
    assert "5.6.7.8" not in app2.active_waiting_clients

# Test: Proxy should redirect non-registered client requests to next available backend instance (port 8001)
def test_proxy_redirect(client):
    client, app2 = client
    response = client.get("/test", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"].startswith("http://testclient:8001/")


# Test: Proxy should correctly forward requests from registered clients, clear them from waiting list, 
# and forward the response back to the client
def test_proxy_registered_client(client, monkeypatch):
    client, app2 = client
    dummy = DummyAsyncClient()
    dummy._resp = MagicMock(status_code=200, text="OK", headers={})
    monkeypatch.setattr("balanced_instance.app2.httpx.AsyncClient", lambda *args, **kwargs: dummy)

    app2.active_waiting_clients.add("testclient")
    response = client.get("/test")
    assert response.status_code == 200
    assert response.text == "OK"
    assert "testclient" not in app2.active_waiting_clients
    assert app2.active_tasks == 0
