import pytest
from httpx import AsyncClient, ASGITransport
from app.main import freelance
from datetime import datetime, timedelta



@pytest.mark.asyncio
async def test_review_crud():
    #Тест CRUD операций для Review
    async with AsyncClient(
        transport=ASGITransport(app=freelance),
        base_url="http://test",
    ) as ac:
        # Подготовка: создаём всё необходимое
        category_response = await ac.post("/category/", json={"category_name": "Programming"})
        category_id = category_response.json()["id"]

        client_data = {
            "first_name": "Client",
            "last_name": "Review",
            "user_name": "clients_review",
            "email": "client_reviewer@example.com",
            "role": "client",
            "password": "password123",
            "created_at": datetime.utcnow().isoformat()
        }
        client_response = await ac.post("/user/", json=client_data)
        reviewer_id = client_response.json()["id"]

        freelancer_data = {
            "first_name": "Freelancers",
            "last_name": "Reviewer",
            "user_name": "freelancerrr_review",
            "email": "freelanrcer@example.com",
            "role": "freelancer",
            "password": "password123",
            "created_at": datetime.utcnow().isoformat()
        }
        freelancer_response = await ac.post("/user/", json=freelancer_data)
        target_id = freelancer_response.json()["id"]

        project_data = {
            "project_name": "API Development",
            "category_id": category_id,
            "client_id": reviewer_id,
            "description": "Need REST API",
            "budget": "3000.00",
            "deadline": (datetime.utcnow() + timedelta(days=20)).isoformat(),
            "status": "completed"
        }
        project_response = await ac.post("/project/", json=project_data)
        project_id = project_response.json()["id"]

        # CREATE REVIEW
        review_data = {
            "rating": 5,
            "comment": "Excellent work, delivered on time!",
            "project_id": project_id,
            "reviewer_id": reviewer_id,
            "target_id": target_id
        }
        response = await ac.post("/reviews/", json=review_data)
        assert response.status_code == 200
        review = response.json()
        assert "id" in review
        review_id = review["id"]
        assert review["rating"] == review_data["rating"]

        # READ (LIST)
        response = await ac.get("/reviews/")
        assert response.status_code == 200
        reviews = response.json()
        assert any(r["id"] == review_id for r in reviews)

        # READ (DETAIL)
        response = await ac.get(f"/reviews/{review_id}")
        assert response.status_code == 200
        review_detail = response.json()
        assert review_detail["id"] == review_id
        assert review_detail["rating"] == review_data["rating"]

        # UPDATE
        update_data = {
            "rating": 4,
            "comment": "Great work, minor delays but overall satisfied"
        }
        response = await ac.put(f"/reviews/{review_id}", json=update_data)
        assert response.status_code == 200
        updated_review = response.json()
        assert updated_review["rating"] == update_data["rating"]
        assert updated_review["comment"] == update_data["comment"]

        # DELETE
        response = await ac.delete(f"/reviews/{review_id}")
        assert response.status_code == 200

        # CONFIRM DELETE
        response = await ac.get(f"/reviews/{review_id}")
        assert response.status_code == 404

        # Cleanup
        await ac.delete(f"/project/{project_id}")
        await ac.delete(f"/user/{target_id}")
        await ac.delete(f"/user/{reviewer_id}")
        await ac.delete(f"/category/{category_id}")