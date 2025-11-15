import pytest
from httpx import AsyncClient, ASGITransport
from app.main import freelance
from datetime import datetime, timedelta


@pytest.mark.asyncio
async def test_project_crud():
    #Тест CRUD операций для Project
    async with AsyncClient(
            transport=ASGITransport(app=freelance),
            base_url="http://test",
    ) as ac:
        # Создаём категорию
        category_data = {"category_name": "Web Development"}
        response = await ac.post("/category/", json=category_data)
        assert response.status_code in [200, 201]
        category_id = response.json()["id"]

        # Создаём пользователя (клиента)
        user_data = {
            "first_name": "Cliesnrt",
            "last_name": "Usersr",
            "user_name": "gpks_2121",
            "email": "gpks@example.com",
            "role": "client",
            "password": "password123"
        }
        response = await ac.post("/user/", json=user_data)

        print(f"\nUser Status: {response.status_code}")
        print(f"User Response: {response.json()}")

        assert response.status_code in [200, 201]  # Принимаем оба статуса
        client_id = response.json()["id"]

        # CREATE PROJECT
        project_data = {
            "project_name": "E-commerce Website",
            "category_id": category_id,
            "client_id": client_id,
            "description": "Need a modern e-commerce website",
            "budget": 5000.00,
            "deadline": (datetime.utcnow() + timedelta(days=30)).isoformat(),
            "status": "open"
        }
        response = await ac.post("/project/", json=project_data)

        print(f"\nProject Status: {response.status_code}")
        print(f"Project Response: {response.json()}")

        assert response.status_code in [200, 201]
        created_project = response.json()
        project_id = created_project["id"]

        # READ
        response = await ac.get(f"/project/{project_id}")
        assert response.status_code == 200
        project = response.json()
        assert project["project_name"] == "E-commerce Website"

        # UPDATE
        update_data = {
            "project_name": "Updated E-commerce Website",
            "budget": 6000.00
        }
        response = await ac.put(f"/project/{project_id}", json=update_data)
        assert response.status_code == 200
        updated_project = response.json()
        assert updated_project["project_name"] == "Updated E-commerce Website"

        # DELETE
        response = await ac.delete(f"/project/{project_id}")
        assert response.status_code == 204

        # Проверяем, что проект удален
        response = await ac.get(f"/project/{project_id}")
        assert response.status_code == 404





