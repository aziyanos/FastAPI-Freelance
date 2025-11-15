import asyncio
from app.db.database import async_session_maker
from sqlalchemy import delete
from app.db.models import (UserProfile, RefreshToken,
                           Project, Review, Category,
                           Skill, Offer)


async def clear_database():
    async with async_session_maker() as session:
        async with session.begin():
            await session.execute(delete(Review))
            await session.execute(delete(Project))
            await session.execute(delete(Category))
            await session.execute(delete(Skill))
            await session.execute(delete(Offer))
            await session.execute(delete(RefreshToken))
            await session.execute(delete(UserProfile))
            await session.commit()
    print("База данных очищена!")

if __name__ == "__main__":
    asyncio.run(clear_database())