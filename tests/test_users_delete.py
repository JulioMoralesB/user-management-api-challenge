import pytest
import uuid


class TestDeleteUser:
    
    # Positive scenarios
    def test_delete_user_success(self, api_client, create_test_user, auth_token):
        email = f"test.{uuid.uuid4().hex[:8]}@example.com"
        create_test_user(email=email, name="Test User", age=25)

        response = api_client.delete(
            f"{api_client.base_url}/users/{email}",
            headers={"Authentication": auth_token}
        )
        assert response.status_code == 204

        # Verify user is deleted
        get_response = api_client.get(f"{api_client.base_url}/users/{email}")
        assert get_response.status_code == 404

    # Negative scenarios
    def test_delete_user_not_found(self, api_client, auth_token):
        email = "nonexistent@example.com"

        response = api_client.delete(
            f"{api_client.base_url}/users/{email}",
            headers={"Authentication": auth_token}
        )
        assert response.status_code == 404
        error = response.json()
        assert "error" in error

    def test_delete_user_missing_auth_header(self, api_client, create_test_user):
        email = f"test.{uuid.uuid4().hex[:8]}@example.com"
        create_test_user(email=email, name="Test User", age=25)

        response = api_client.delete(f"{api_client.base_url}/users/{email}")
        assert response.status_code == 401
        error = response.json()
        assert "error" in error

    def test_delete_user_invalid_auth_token(self, api_client, create_test_user):
        email = f"test.{uuid.uuid4().hex[:8]}@example.com"
        create_test_user(email=email, name="Test User", age=25)

        response = api_client.delete(
            f"{api_client.base_url}/users/{email}",
            headers={"Authentication": "wrongtoken"}
        )
        assert response.status_code == 401
        error = response.json()
        assert "error" in error

    def test_delete_user_empty_auth_header(self, api_client, create_test_user):
        email = f"test.{uuid.uuid4().hex[:8]}@example.com"
        create_test_user(email=email, name="Test User", age=25)

        response = api_client.delete(
            f"{api_client.base_url}/users/{email}",
            headers={"Authentication": ""}
        )
        assert response.status_code == 401
        error = response.json()
        assert "error" in error

    def test_delete_already_deleted_user(self, api_client, create_test_user, auth_token):
        email = f"test.{uuid.uuid4().hex[:8]}@example.com"
        create_test_user(email=email, name="Test User", age=25)

        # Delete once
        response1 = api_client.delete(
            f"{api_client.base_url}/users/{email}",
            headers={"Authentication": auth_token}
        )
        assert response1.status_code == 204

        # Try to delete again
        response2 = api_client.delete(
            f"{api_client.base_url}/users/{email}",
            headers={"Authentication": auth_token}
        )
        assert response2.status_code == 404
