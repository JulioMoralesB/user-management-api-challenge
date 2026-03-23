import pytest
import uuid


class TestGetUserByEmail:
    # Positive scenarios
    def test_get_user_by_email_success(self, api_client, create_test_user):
        email = f"test.{uuid.uuid4().hex[:8]}@example.com"
        create_test_user(email=email, name="Jane Doe", age=28)

        response = api_client.get(f"{api_client.base_url}/users/{email}")
        assert response.status_code == 200
        user = response.json()

        assert user["email"] == email
        assert user["name"] == "Jane Doe"
        assert user["age"] == 28
    
    # Negative scenarios
    def test_get_user_by_email_not_found(self, api_client):
        email = "nonexistent@example.com"

        response = api_client.get(f"{api_client.base_url}/users/{email}")
        assert response.status_code == 404
        error = response.json()
        assert "error" in error

    def test_get_user_by_email_invalid_email_format(self, api_client):
        response = api_client.get(f"{api_client.base_url}/users/not-an-email")
        assert response.status_code in [400, 404]
