import pytest


class TestListUsers:

    def test_list_users_returns_users(self, api_client, create_test_user):
        # Create a user
        user_data = create_test_user(email="user1@example.com", name="User One", age=25)

        # List users
        response = api_client.get(f"{api_client.base_url}/users")
        assert response.status_code == 200
        users = response.json()
        assert isinstance(users, list)

        # Find the created user in the list
        found_user = next((u for u in users if u["email"] == "user1@example.com"), None)
        assert found_user is not None
        assert found_user["name"] == "User One"
        assert found_user["age"] == 25

    def test_list_users_multiple(self, api_client, create_test_user):
        # Create multiple users
        user1 = create_test_user(email="user1@example.com", name="User One", age=25)
        user2 = create_test_user(email="user2@example.com", name="User Two", age=35)

        # List users
        response = api_client.get(f"{api_client.base_url}/users")
        assert response.status_code == 200
        users = response.json()

        emails = [u["email"] for u in users]
        assert "user1@example.com" in emails
        assert "user2@example.com" in emails
