import pytest
import requests
import os
import logging
import json
from typing import Dict, Any


logger = logging.getLogger(__name__)

# Configuration
BASE_URL = os.getenv("API_BASE_URL", "http://localhost:3000")
AUTH_TOKEN = "mysecrettoken"
ENVIRONMENTS = ["dev", "prod"]


@pytest.fixture(scope="session")
def api_base_url():
    """Return the base URL for the API."""
    return BASE_URL


@pytest.fixture(scope="session")
def auth_token():
    """Return the authentication token."""
    return AUTH_TOKEN


@pytest.fixture(params=ENVIRONMENTS)
def environment(request):
    """Parametrize tests to run against both dev and prod environments."""
    return request.param


@pytest.fixture
def api_url(api_base_url, environment):
    """Return the full API URL for the given environment."""
    return f"{api_base_url}/{environment}"


def log_request_response(method: str, url: str, request_body=None, response=None, headers=None):
    """Log HTTP request and response details for debugging."""
    logger.info(f"\n{'='*80}")
    logger.info(f"HTTP {method} {url}")
    if headers:
        logger.info(f"Headers: {dict(headers)}")
    if request_body:
        try:
            logger.info(f"Request Body: {json.dumps(request_body, indent=2)}")
        except:
            logger.info(f"Request Body: {request_body}")
    
    if response is not None:
        logger.info(f"Status: {response.status_code}")
        try:
            response_data = response.json()
            logger.info(f"Response Body: {json.dumps(response_data, indent=2)}")
        except:
            logger.info(f"Response Body: {response.text}")
    logger.info(f"{'='*80}")


class LoggingSession(requests.Session):
    """Custom session that logs all requests and responses."""
    
    def __init__(self, base_url=None):
        super().__init__()
        self.base_url = base_url
    
    def request(self, method, url, **kwargs):
        """Override request to log HTTP interactions."""
        full_url = f"{self.base_url}{url}" if self.base_url and not url.startswith('http') else url
        headers = kwargs.get('headers', {})
        json_data = kwargs.get('json')
        
        response = super().request(method, url, **kwargs)
        
        log_request_response(method, full_url, request_body=json_data, response=response, headers=headers)
        
        return response


@pytest.fixture
def api_client(api_url):
    """Return a session with base URL pre-configured and logging enabled."""
    session = LoggingSession(base_url=api_url)
    return session


@pytest.fixture
def create_test_user(api_client):
    """Factory fixture to create test users."""
    created_users = []

    def _create_user(name: str = "Test User", email: str = None, age: int = 30) -> Dict[str, Any]:
        if email is None:
            import uuid
            email = f"test.{uuid.uuid4().hex[:8]}@example.com"

        payload = {"name": name, "email": email, "age": age}
        response = api_client.post(f"{api_client.base_url}/users", json=payload)
        response.raise_for_status()
        user = response.json()
        created_users.append({"email": email, "url": f"{api_client.base_url}/users/{email}"})
        return user

    yield _create_user

    # Cleanup: delete all created users
    for user in created_users:
        try:
            api_client.delete(user["url"], headers={"Authentication": AUTH_TOKEN})
        except Exception:
            pass  # Ignore cleanup errors


@pytest.fixture
def test_user_email(api_client):
    """Provide a test user email with cleanup."""
    import uuid
    email = f"test.{uuid.uuid4().hex[:8]}@example.com"

    # Create the user
    payload = {"name": "Test User", "email": email, "age": 30}
    api_client.post(f"{api_client.base_url}/users", json=payload)

    yield email

    # Cleanup
    try:
        api_client.delete(
            f"{api_client.base_url}/users/{email}",
            headers={"Authentication": AUTH_TOKEN}
        )
    except Exception:
        pass


@pytest.fixture
def valid_user_payload() -> Dict[str, Any]:
    import uuid
    return {
        "name": "Jane Doe",
        "email": f"jane.{uuid.uuid4().hex[:8]}@example.com",
        "age": 30
    }


@pytest.fixture
def invalid_user_payloads() -> Dict[str, Dict[str, Any]]:
    """Return various invalid user payloads for validation testing."""
    return {
        "invalid_email": {
            "name": "Test User",
            "email": "not-an-email",
            "age": 30
        },
        "age_too_low": {
            "name": "Test User",
            "email": "test@example.com",
            "age": 0
        },
        "age_too_high": {
            "name": "Test User",
            "email": "test@example.com",
            "age": 151
        },
        "age_negative": {
            "name": "Test User",
            "email": "test@example.com",
            "age": -5
        },
        "empty_name": {
            "name": "",
            "email": "test@example.com",
            "age": 30
        }
    }
