from fastapi import FastAPI, APIRouter
from starlette.responses import HTMLResponse
from app.db.database import SessionLocal
import uvicorn
from datetime import datetime
from app.api import (skills, users, categories,
                     projects, offers, reviews)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


freelance = FastAPI()

freelance.include_router(skills.skill_router)
freelance.include_router(users.user_router)
freelance.include_router(categories.category_router)
freelance.include_router(projects.project_router)
freelance.include_router(offers.offer_router)
freelance.include_router(reviews.review_router)


@freelance.get("/health/")
async def health_check():
    return {
        "status": "ok",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }



@freelance.get("/", response_class=HTMLResponse)
async def Home():
    return """
    <html>
        <head>
            <title>Booking</title>
        </head>
        <body>
            <h1>Salam Aleikum</h1>
            <p>Документация: <a href="/docs">Swagger</a></p>
        </body>
    </html>
    """


if __name__ == '__main__':
    uvicorn.run(freelance, host='127.0.0.1', port=8001)