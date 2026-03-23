import pytest
import uuid


class TestUpdateUser:
    # Positive scenarios
    def test_update_user_success(self, api_client, create_test_user):
        email = f"test.{uuid.uuid4().hex[:8]}@example.com"
        create_test_user(email=email, name="Original Name", age=25)

        # Update the user
        payload = {
            "name": "Updated Name",
            "email": email,
            "age": 35
        }
        response = api_client.put(f"{api_client.base_url}/users/{email}", json=payload)
        assert response.status_code == 200
        user = response.json()

        assert user["name"] == "Updated Name"
        assert user["email"] == email
        assert user["age"] == 35
        
    def test_update_user_minimum_age(self, api_client, create_test_user):
        email = f"test.{uuid.uuid4().hex[:8]}@example.com"
        create_test_user(email=email, name="Test", age=25)

        payload = {
            "name": "Updated",
            "email": email,
            "age": 1
        }
        response = api_client.put(f"{api_client.base_url}/users/{email}", json=payload)
        assert response.status_code == 200
        user = response.json()
        assert user["age"] == 1

    def test_update_user_maximum_age(self, api_client, create_test_user):
        email = f"test.{uuid.uuid4().hex[:8]}@example.com"
        create_test_user(email=email, name="Test", age=25)

        payload = {
            "name": "Updated",
            "email": email,
            "age": 150
        }
        response = api_client.put(f"{api_client.base_url}/users/{email}", json=payload)
        assert response.status_code == 200
        user = response.json()
        assert user["age"] == 150

    # Negative scenarios
    def test_update_user_not_found(self, api_client):
        email = "nonexistent@example.com"
        payload = {
            "name": "Updated Name",
            "email": email,
            "age": 35
        }

        response = api_client.put(f"{api_client.base_url}/users/{email}", json=payload)
        assert response.status_code == 404
        error = response.json()
        assert "error" in error

    def test_update_user_missing_name(self, api_client, create_test_user):
        email = f"test.{uuid.uuid4().hex[:8]}@example.com"
        create_test_user(email=email, name="Test", age=25)

        payload = {
            "email": email,
            "age": 35
        }
        response = api_client.put(f"{api_client.base_url}/users/{email}", json=payload)
        assert response.status_code == 400
        error = response.json()
        assert "error" in error

    def test_update_user_missing_email(self, api_client, create_test_user):
        email = f"test.{uuid.uuid4().hex[:8]}@example.com"
        create_test_user(email=email, name="Test", age=25)

        payload = {
            "name": "Updated",
            "age": 35
        }
        response = api_client.put(f"{api_client.base_url}/users/{email}", json=payload)
        assert response.status_code == 400
        error = response.json()
        assert "error" in error

    def test_update_user_missing_age(self, api_client, create_test_user):
        email = f"test.{uuid.uuid4().hex[:8]}@example.com"
        create_test_user(email=email, name="Test", age=25)

        payload = {
            "name": "Updated",
            "email": email
        }
        response = api_client.put(f"{api_client.base_url}/users/{email}", json=payload)
        assert response.status_code == 400
        error = response.json()
        assert "error" in error

    def test_update_user_invalid_email_format(self, api_client, create_test_user):
        email = f"test.{uuid.uuid4().hex[:8]}@example.com"
        create_test_user(email=email, name="Test", age=25)

        payload = {
            "name": "Updated",
            "email": "not-an-email",
            "age": 35
        }
        response = api_client.put(f"{api_client.base_url}/users/{email}", json=payload)
        assert response.status_code == 400
        error = response.json()
        assert "error" in error

    def test_update_user_age_too_low(self, api_client, create_test_user):
        email = f"test.{uuid.uuid4().hex[:8]}@example.com"
        create_test_user(email=email, name="Test", age=25)

        payload = {
            "name": "Updated",
            "email": email,
            "age": 0
        }
        response = api_client.put(f"{api_client.base_url}/users/{email}", json=payload)
        assert response.status_code == 400
        error = response.json()
        assert "error" in error

    def test_update_user_age_too_high(self, api_client, create_test_user):
        email = f"test.{uuid.uuid4().hex[:8]}@example.com"
        create_test_user(email=email, name="Test", age=25)

        payload = {
            "name": "Updated",
            "email": email,
            "age": 151
        }
        response = api_client.put(f"{api_client.base_url}/users/{email}", json=payload)
        assert response.status_code == 400
        error = response.json()
        assert "error" in error

    def test_update_user_age_negative(self, api_client, create_test_user):
        email = f"test.{uuid.uuid4().hex[:8]}@example.com"
        create_test_user(email=email, name="Test", age=25)

        payload = {
            "name": "Updated",
            "email": email,
            "age": -5
        }
        response = api_client.put(f"{api_client.base_url}/users/{email}", json=payload)
        assert response.status_code == 400
        error = response.json()
        assert "error" in error

    def test_update_user_change_email_to_duplicate(self, api_client, create_test_user):
        email1 = f"test1.{uuid.uuid4().hex[:8]}@example.com"
        email2 = f"test2.{uuid.uuid4().hex[:8]}@example.com"

        # Create two users
        create_test_user(email=email1, name="User One", age=25)
        create_test_user(email=email2, name="User Two", age=30)

        # Try to update email1's email to email2 (duplicate)
        payload = {
            "name": "Updated",
            "email": email2,
            "age": 35
        }
        response = api_client.put(f"{api_client.base_url}/users/{email1}", json=payload)
        assert response.status_code == 409
        error = response.json()
        assert "error" in error

    def test_update_user_empty_name(self, api_client, create_test_user):
        """Test updating user with empty name."""
        email = f"test.{uuid.uuid4().hex[:8]}@example.com"
        create_test_user(email=email, name="Test", age=25)

        payload = {
            "name": "",
            "email": email,
            "age": 35
        }
        response = api_client.put(f"{api_client.base_url}/users/{email}", json=payload)
        assert response.status_code == 400
        error = response.json()
        assert "error" in error
