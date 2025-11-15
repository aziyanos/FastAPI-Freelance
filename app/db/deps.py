from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import async_session_maker


#Используйте flush() в endpoints, а не refresh()
async def get_db() -> AsyncGenerator[AsyncSession, None]: #SQLAlchemy 2.0
    """
    Dependency для получения async DB сессии.

    Используется через FastAPI Depends():
        @router.get("/")
        async def endpoint(db: AsyncSession = Depends(get_db)):
            ...

    Yields:
        AsyncSession: Асинхронная сессия SQLAlchemy

    Note:
        - Автоматический commit при успехе (session.begin())
        - Автоматический rollback при ошибке
        - Гарантированное закрытие сессии (finally)
    """
    async with async_session_maker() as session:
        async with session.begin(): #Автоматический db.commit/rollback
            yield session