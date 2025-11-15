from fastapi import FastAPI, APIRouter
from starlette.responses import HTMLResponse
from app.db.database import async_session_maker
import uvicorn
from datetime import datetime
from app.api import (skills, users, categories, auth,
                     projects, offers, reviews,)
#from app.middlewares.middleware import LoggingMiddleware
from app.middlewares.middleware import logging_middleware
from app.admin.setup import setup_admin



async def get_db():
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


freelance = FastAPI()

freelance.include_router(skills.skill_router)
freelance.include_router(users.user_router)
freelance.include_router(auth.auth_router)
freelance.include_router(categories.category_router)
freelance.include_router(projects.project_router)
freelance.include_router(offers.offer_router)
freelance.include_router(reviews.review_router)

setup_admin(freelance)


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

@freelance.middleware("http")
async def custom_logging_middleware(request, call_next):
    return await logging_middleware(request, call_next)



if __name__ == '__main__':
    uvicorn.run(freelance, host='127.0.0.1', port=8001)


