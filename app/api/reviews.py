from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter
from typing import List
from app.db.database import SessionLocal
from app.db.schemas import ReviewSchema
from app.db.models import Review


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


review_router = APIRouter(prefix="/reviews", tags=["Reviews"])


@review_router.get('/', response_model=List[ReviewSchema])
async def list_reviews(db: Session = Depends(get_db)):
    review_db = db.query(Review).all()
    return review_db


@review_router.post('/', response_model=ReviewSchema)
async def create_review(review_create: ReviewSchema,
                        db: Session = Depends(get_db)):
    new_review = Review(**review_create.dict())
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


@review_router.get('/{review_id}', response_model=ReviewSchema)
async def detail_review(review_id: int, db: Session
                        =Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if not review_db:
        raise HTTPException(status_code=404, detail="Review not found")
    return review_db


@review_router.put('/{review_id}', response_model=ReviewSchema)
async def update_review(review_id: int, review_update: ReviewSchema,
                        db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if not review_db:
        raise HTTPException(status_code=404, detail="Review not found")
    for key, value in review_update.dict().items():
        setattr(review_db, key, value)
    db.commit()
    db.refresh(review_db)
    return review_db


@review_router.delete('/{review_id}')
async def delete_review(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if not review_db:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(review_db)
    db.commit()
    return {'message': 'Review deleted'}



