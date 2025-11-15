#########################################################
from fastapi import HTTPException, Depends, APIRouter
from starlette import status
from starlette.responses import Response
from app.db.models import UserProfile
from app.db.schemas import (UserProfileOutSchema,
                            UserProfileUpdateSchema,
                            UserProfileDetailSchema,
                            UserProfileCreateSchema)
from app.db.database import async_session_maker
from typing import List, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select



#Используйте flush() в endpoints, а не refresh()
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        async with session.begin():
            yield session


user_router = APIRouter(prefix='/user', tags=['UserProfile'])


@user_router.get('/', response_model=List[UserProfileOutSchema])
async def list_user(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserProfile))
    user_db = result.scalars().all()
    return user_db


@user_router.post('/', response_model=UserProfileOutSchema)
async def create_user(user_create: UserProfileCreateSchema,
                      db: AsyncSession = Depends(get_db)):
    user_db = UserProfile(**user_create.model_dump())
    db.add(user_db)
    await db.flush()
    return user_db


@user_router.get('/{user_id}', response_model=UserProfileDetailSchema)
async def detail_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserProfile).filter(UserProfile.id == user_id))
    user_db = result.scalar_one_or_none()
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found')
    return user_db


@user_router.put('/{user_id}', response_model=UserProfileOutSchema)
async def update_user(user_id: int, user_update: UserProfileUpdateSchema,
                      db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserProfile).filter(UserProfile.id == user_id))
    user_db = result.scalar_one_or_none()
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found'
                            )
    for user_key, user_value in user_update.dict(exclude_unset=True).items():
        setattr(user_db, user_key, user_value)

    db.add(user_db)
    await db.flush()
    return user_db


@user_router.delete('/{user_id}')
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserProfile).filter(UserProfile.id == user_id))
    user_db = result.scalar_one_or_none()
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found')
    await db.delete(user_db)
    await db.flush()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


























