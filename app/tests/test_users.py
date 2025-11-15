import asyncio

import pytest
from httpx import AsyncClient, ASGITransport, delete
from app.main import freelance
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from app.db.models import UserProfile, RefreshToken



@pytest.mark.asyncio
async def test_user_crud():
    #Тест CRUD операций для UserProfile
    async with AsyncClient(
        transport=ASGITransport(app=freelance),
        base_url="http://test",
    ) as ac:
        # CREATE
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "user_name": "johndoe",
            "email": "john@example.com",
            "age": 30,
            "phone_number": "+996555123456",
            "role": "freelancer",
            "password": "password123",
            "created_at": datetime.utcnow().isoformat()

        }
        response = await ac.post("/user/", json=user_data)
        assert response.status_code == 200
        user = response.json()
        assert "id" in user
        user_id = user["id"]
        assert user["user_name"] == user_data["user_name"]

        # READ (LIST)
        response = await ac.get("/user/")
        assert response.status_code == 200
        users = response.json()
        assert any(u["id"] == user_id for u in users)

        # READ (DETAIL)
        response = await ac.get(f"/user/{user_id}")
        assert response.status_code == 200
        user_detail = response.json()
        assert user_detail["id"] == user_id
        assert user_detail["user_name"] == user_data["user_name"]

        # UPDATE
        update_data = {"first_name": "Jane", "age": 31}
        response = await ac.put(f"/user/{user_id}", json=update_data)
        assert response.status_code == 200
        updated_user = response.json()
        assert updated_user["first_name"] == update_data["first_name"]
        assert updated_user["age"] == update_data["age"]

        # DELETE
        response = await ac.delete(f"/user/{user_id}")
        assert response.status_code == 204

        # CONFIRM DELETE
        response = await ac.get(f"/user/{user_id}")
        assert response.status_code == 404

