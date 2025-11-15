
import pytest

from httpx import AsyncClient, ASGITransport
from app.main import freelance



@pytest.mark.asyncio
async def test_category_crud():
    async with AsyncClient(
        transport=ASGITransport(app=freelance),
        base_url="http://test",
    ) as ac:

        # CREATE

        category_data = {"category_name": "Test Category"}
        response = await ac.post("/category/", json=category_data)
        assert response.status_code == 200
        category = response.json()
        assert "id" in category
        category_id = category["id"]
        assert category["category_name"] == category_data["category_name"]


        # READ (LIST)

        response = await ac.get("/category/")
        assert response.status_code == 200
        categories = response.json()
        assert any(c["id"] == category_id for c in categories)


        # READ (DETAIL)

        response = await ac.get(f"/category/{category_id}")
        assert response.status_code == 200
        category_detail = response.json()
        assert category_detail["id"] == category_id
        assert category_detail["category_name"] == category_data["category_name"]


        # UPDATE

        update_data = {"category_name": "Updated Category"}
        response = await ac.put(f"/category/{category_id}", json=update_data)
        assert response.status_code == 200
        updated_category = response.json()
        assert updated_category["category_name"] == update_data["category_name"]


        # DELETE

        response = await ac.delete(f"/category/{category_id}")
        assert response.status_code == 200
        delete_response = response.json()
        assert delete_response["message"] == "Category deleted"


        # CONFIRM DELETE

        response = await ac.get(f"/category/{category_id}")
        assert response.status_code == 404

