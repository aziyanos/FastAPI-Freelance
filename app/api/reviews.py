from fastapi import Depends, HTTPException, APIRouter
from typing import List, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.database import async_session_maker
from app.db.schemas import (ReviewOutSchema, ReviewCreateSchema,
                            ReviewUpdateSchema, ReviewDetailSchema)
from app.db.models import Review
from app.db.deps import get_db


review_router = APIRouter(prefix="/reviews", tags=["Reviews"])


@review_router.get('/', response_model=List[ReviewOutSchema])
async def list_reviews(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Review))
    review_db = result.scalars().all()
    return review_db


@review_router.post('/', response_model=ReviewOutSchema)
async def create_review(review_create: ReviewCreateSchema,
                        db: AsyncSession = Depends(get_db)):
    new_review = Review(**review_create.model_dump()) #в место dict, model_dump новая версия sqlal
    db.add(new_review)
    await db.flush()
    return new_review


@review_router.get('/{review_id}', response_model=ReviewDetailSchema)
async def detail_review(review_id: int, db: AsyncSession
                                                    =Depends(get_db)):
    result = await db.execute(select(Review).filter(Review.id == review_id))
    review_db = result.scalar_one_or_none()
    if not review_db:
        raise HTTPException(status_code=404, detail="Review not found")
    return review_db


@review_router.put('/{review_id}', response_model=ReviewOutSchema)
async def update_review(review_id: int, review_update: ReviewUpdateSchema,
                        db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Review).filter(Review.id == review_id))
    review_db = result.scalar_one_or_none()
    if not review_db:
        raise HTTPException(status_code=404, detail="Review not found")
    for key, value in review_update.dict(exclude_unset=True).items():
        setattr(review_db, key, value)
    await db.flush()
    return review_db


@review_router.delete('/{review_id}')
async def delete_review(review_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Review).filter(Review.id == review_id))
    review_db = result.scalar_one_or_none()
    if not review_db:
        raise HTTPException(status_code=404, detail="Review not found")
    await db.delete(review_db)
    await db.flush()
    return {'message': 'Review deleted'}



