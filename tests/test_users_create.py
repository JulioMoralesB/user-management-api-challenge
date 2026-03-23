import pytest
import uuid


class TestCreateUser:
    # Positive scenarios
    def test_create_user_success(self, api_client, valid_user_payload):
        
        response = api_client.post(f"{api_client.base_url}/users", json=valid_user_payload)
        assert response.status_code == 201
        user = response.json()

        assert user["name"] == valid_user_payload["name"]
        assert user["email"] == valid_user_payload["email"]
        assert user["age"] == valid_user_payload["age"]

        # Cleanup
        api_client.delete(
            f"{api_client.base_url}/users/{valid_user_payload['email']}",
            headers={"Authentication": "mysecrettoken"}
        )

    def test_create_user_minimum_age(self, api_client, valid_user_payload):
        valid_user_payload["age"] = 1

        response = api_client.post(f"{api_client.base_url}/users", json=valid_user_payload)
        assert response.status_code == 201
        user = response.json()
        assert user["age"] == 1

        # Cleanup
        api_client.delete(
            f"{api_client.base_url}/users/{valid_user_payload['email']}",
            headers={"Authentication": "mysecrettoken"}
        )

    def test_create_user_maximum_age(self, api_client, valid_user_payload):
        valid_user_payload["age"] = 150

        response = api_client.post(f"{api_client.base_url}/users", json=valid_user_payload)
        assert response.status_code == 201
        user = response.json()
        assert user["age"] == 150

        # Cleanup
        api_client.delete(
            f"{api_client.base_url}/users/{valid_user_payload['email']}",
            headers={"Authentication": "mysecrettoken"}
        )

    # Negative scenarios
    def test_create_user_duplicate_email(self, api_client, create_test_user):

        email = f"duplicate.{uuid.uuid4().hex[:8]}@example.com"
        create_test_user(email=email, name="First User", age=25)

        payload = {
            "name": "Second User",
            "email": email,
            "age": 30
        }
        response = api_client.post(f"{api_client.base_url}/users", json=payload)
        assert response.status_code == 409
        error = response.json()
        assert "error" in error

    def test_create_user_missing_name(self, api_client, valid_user_payload):
        
        valid_user_payload.pop("name")
        
        response = api_client.post(f"{api_client.base_url}/users", json=valid_user_payload)
        assert response.status_code == 400
        error = response.json()
        assert "error" in error

    def test_create_user_missing_email(self, api_client, valid_user_payload):
        
        valid_user_payload.pop("email")

        response = api_client.post(f"{api_client.base_url}/users", json=valid_user_payload)
        assert response.status_code == 400
        error = response.json()
        assert "error" in error

    def test_create_user_missing_age(self, api_client, valid_user_payload):
        
        valid_user_payload.pop("age")

        response = api_client.post(f"{api_client.base_url}/users", json=valid_user_payload)
        assert response.status_code == 400
        error = response.json()
        assert "error" in error

    def test_create_user_invalid_email_format(self, api_client, invalid_user_payloads):
        
        payload = invalid_user_payloads["invalid_email"]

        response = api_client.post(f"{api_client.base_url}/users", json=payload)
        assert response.status_code == 400
        error = response.json()
        assert "error" in error

    def test_create_user_age_too_low(self, api_client, invalid_user_payloads):
        
        payload = invalid_user_payloads["age_too_low"]

        response = api_client.post(f"{api_client.base_url}/users", json=payload)
        assert response.status_code == 400
        error = response.json()
        assert "error" in error

    def test_create_user_age_too_high(self, api_client, invalid_user_payloads):
        
        payload = invalid_user_payloads["age_too_high"]

        response = api_client.post(f"{api_client.base_url}/users", json=payload)
        assert response.status_code == 400
        error = response.json()
        assert "error" in error

    def test_create_user_age_negative(self, api_client, invalid_user_payloads):
        
        payload = invalid_user_payloads["age_negative"]

        response = api_client.post(f"{api_client.base_url}/users", json=payload)
        assert response.status_code == 400
        error = response.json()
        assert "error" in error

    def test_create_user_empty_name(self, api_client, invalid_user_payloads):
        payload = invalid_user_payloads["empty_name"]

        response = api_client.post(f"{api_client.base_url}/users", json=payload)
        assert response.status_code == 400
        error = response.json()
        assert "error" in error


