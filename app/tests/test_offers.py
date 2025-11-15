import pytest
from httpx import AsyncClient, ASGITransport
from app.main import freelance
from datetime import datetime, timedelta




@pytest.mark.asyncio
async def test_offer_crud():
    #Тест CRUD операций для Offer
    async with AsyncClient(
        transport=ASGITransport(app=freelance),
        base_url="http://test",
    ) as ac:
        # Подготовка: создаём категорию, клиента, фрилансера и проект
        category_response = await ac.post("/category/", json={"category_name": "Design"})
        category_id = category_response.json()["id"]

        client_data = {
            "first_name": "Client",
            "last_name": "User",
            "user_name": "client_offer",
            "email": "client_ooffer@example.com",
            "role": "client",
            "password": "password123",
            "created_at": datetime.utcnow().isoformat()
        }
        client_response = await ac.post("/user/", json=client_data)
        client_id = client_response.json()["id"]

        freelancer_data = {
            "first_name": "Freelancer",
            "last_name": "User",
            "user_name": "freelancer_offer",
            "email": "freelancer_offer@example.com",
            "role": "freelancer",
            "password": "password123",
            "created_at": datetime.utcnow().isoformat()
        }
        freelancer_response = await ac.post("/user/", json=freelancer_data)
        freelancer_id = freelancer_response.json()["id"]

        project_data = {
            "project_name": "Logo Design",
            "category_id": category_id,
            "client_id": client_id,
            "description": "Need a professional logo",
            "budget": "1000.00",
            "deadline": (datetime.utcnow() + timedelta(days=15)).isoformat(),
            "status": "open"
        }
        project_response = await ac.post("/project/", json=project_data)
        project_id = project_response.json()["id"]

        # CREATE
        offer_data = {
            "message": "I can create an amazing logo for you",
            "proposed_budget": "900.00",
            "proposed_deadline": (datetime.utcnow() + timedelta(days=10)).isoformat(),
            "project_id": project_id,
            "freelancer_id": freelancer_id
        }
        response = await ac.post("/offers/", json=offer_data)
        assert response.status_code == 200
        offer = response.json()
        assert "id" in offer
        offer_id = offer["id"]
        assert offer["message"] == offer_data["message"]

        # READ (LIST)
        response = await ac.get("/offers/")
        assert response.status_code == 200
        offers = response.json()
        assert any(o["id"] == offer_id for o in offers)

        # READ (DETAIL)
        response = await ac.get(f"/offers/{offer_id}")
        assert response.status_code == 200
        offer_detail = response.json()
        assert offer_detail["id"] == offer_id
        assert offer_detail["message"] == offer_data["message"]

        # UPDATE
        update_data = {
            "message": "I can create an amazing logo for you with revisions",
            "proposed_budget": "850.00"
        }
        response = await ac.put(f"/offers/{offer_id}", json=update_data)
        assert response.status_code == 200
        updated_offer = response.json()
        assert updated_offer["message"] == update_data["message"]

        # DELETE
        response = await ac.delete(f"/offers/{offer_id}")
        assert response.status_code == 200

        # CONFIRM DELETE
        response = await ac.get(f"/offers/{offer_id}")
        assert response.status_code == 404

        # Cleanup
        #await ac.delete(f"/project/{project_id}")
        #await ac.delete(f"/user/{freelancer_id}")
        #await ac.delete(f"/user/{client_id}")
        #await ac.delete(f"/category/{category_id}")