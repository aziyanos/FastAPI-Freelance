from fastapi import HTTPException, Depends, APIRouter
from starlette import status
from starlette.responses import Response
from app.db.models import UserProfile
from app.db.schemas import (UserProfileOutSchema,
                            UserProfileUpdateSchema,
                            UserProfileDetailSchema,
                            UserProfileCreateSchema)
from app.db.database import SessionLocal
from sqlalchemy.orm import Session
from typing import List


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


user_router = APIRouter(prefix='/user', tags=['UserProfile'])


@user_router.get('/', response_model=List[UserProfileOutSchema])
async def list_user(db: Session = Depends(get_db)):
    return db.query(UserProfile).all()


@user_router.post('/', response_model=UserProfileOutSchema)
async def create_user(user_data: UserProfileCreateSchema,
                      db: Session = Depends(get_db)):
    user_db = UserProfile(**user_data.dict())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


@user_router.get('/{user_id}', response_model=UserProfileDetailSchema)
async def detail_user(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found')
    return user_db


@user_router.put('/{user_id}', response_model=UserProfileOutSchema)
async def update_user(user_id: int, user_data: UserProfileUpdateSchema,
                      db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found'
                            )
    for user_key, user_value in user_data.dict().items():
        setattr(user_db, user_key, user_value)

    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


@user_router.delete('/{user_id}')
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found')
    db.delete(user_db)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)






