from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from app.db.database import AsyncSession, async_session_maker
from fastapi import APIRouter, Depends
from starlette.requests import Request
from app.config import settings
from authlib.integrations.starlette_client import OAuth
from typing import AsyncGenerator


oauth = OAuth()
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_KEY,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    client_kwargs={'scope': 'openid email profile'},
)

oauth.register(
    name='github',
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_KEY,
    authorize_url='https://github.com/login/oauth/authorize',
)

social_router = APIRouter(prefix='/oauth', tags=['OAuth'])

#Используйте flush() в endpoints, а не refresh()
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        async with session.begin(): # ← Автоматический db.commit/rollback
            yield session


@social_router.get('/google')
async def google_login(request: Request):
    redirect_url = settings.GOOGLE_LOGIN_CALLBACK
    return await oauth.google.authorize_redirect(request, redirect_url)

@social_router.get('/github')
async def github_login(request: Request):
    redirect_url = settings.GITHUB_LOGIN_CALLBACK
    return await oauth.github.authorize_redirect(request, redirect_url)