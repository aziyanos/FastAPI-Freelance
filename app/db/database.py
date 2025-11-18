from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (create_async_engine,
                                    async_sessionmaker,
                                    AsyncSession)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator
import os
load_dotenv()

DB_URL = os.getenv('DB_URL')

engine = create_async_engine(DB_URL, echo=True)

async_session_maker = async_sessionmaker(engine, class_=AsyncSession,
                                         expire_on_commit=False)



#Base (современный способ)
class Base(DeclarativeBase):
    pass


# Dependency для FastAPI
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

