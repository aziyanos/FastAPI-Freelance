
import pytest

from httpx import AsyncClient, ASGITransport
from app.main import freelance


@pytest.fixture
async def test_user(test_client):
    """Создать тестового пользователя"""
    user_data = {
        "user_name": "testuser",
        "email": "test@example.com",
        "password": "Test123!",
        "role": "client"
    }
    response = await test_client.post("/auth/register", json=user_data)
    return response.json()

@pytest.fixture
async def auth_client(test_client, test_user):
    """Аутентифицированный клиент"""
    login_data = {
        "user_name": "testuser",
        "password": "Test123!"
    }
    response = await test_client.post("/auth/login", json=login_data)
    token = response.json()["access_token"]
    test_client.headers["Authorization"] = f"Bearer {token}"
    return test_client

# ✅ app/tests/test_auth.py
@pytest.mark.asyncio
async def test_protected_endpoint(auth_client):
    response = await auth_client.get("/user/me")
    assert response.status_code == 200