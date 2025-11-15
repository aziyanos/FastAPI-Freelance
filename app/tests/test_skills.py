import pytest
from httpx import AsyncClient, ASGITransport
from app.main import freelance
from datetime import datetime, timedelta
from decimal import Decimal


@pytest.mark.asyncio
async def test_skill_crud():
    #Тест CRUD операций для Skill
    async with AsyncClient(
        transport=ASGITransport(app=freelance),
        base_url="http://test",
    ) as ac:
        # CREATE
        skill_data = {"skill_name": "Python"}
        response = await ac.post("/skill/", json=skill_data)
        assert response.status_code == 200
        skill = response.json()
        assert "id" in skill
        skill_id = skill["id"]
        assert skill["skill_name"] == skill_data["skill_name"]

        # READ (LIST)
        response = await ac.get("/skill/")
        assert response.status_code == 200
        skills = response.json()
        assert any(s["id"] == skill_id for s in skills)

        # READ (DETAIL)
        response = await ac.get(f"/skill/{skill_id}")
        assert response.status_code == 200
        skill_detail = response.json()
        assert skill_detail["id"] == skill_id
        assert skill_detail["skill_name"] == skill_data["skill_name"]

        # UPDATE
        update_data = {"skill_name": "Python Advanced"}
        response = await ac.put(f"/skill/{skill_id}", json=update_data)
        assert response.status_code == 200
        updated_skill = response.json()
        assert updated_skill["skill_name"] == update_data["skill_name"]

        # DELETE
        response = await ac.delete(f"/skill/{skill_id}")
        assert response.status_code == 200

        # CONFIRM DELETE
        response = await ac.get(f"/skill/{skill_id}")
        assert response.status_code == 404