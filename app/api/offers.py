from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.db.database import SessionLocal
from app.db.schemas import (OfferOutSchema, OfferCreateSchema,
                            OfferUpdateSchema, OfferDetailSchema)
from app.db.models import Offer


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


offer_router = APIRouter(prefix="/offers", tags=["Offers"])


@offer_router.get("/", response_model=List[OfferOutSchema])
async def list_offers(db: Session = Depends(get_db)):
    offers = db.query(Offer).all()
    return offers


@offer_router.post("/", response_model=OfferOutSchema)
async def create_offer(offer_create: OfferCreateSchema,
                       db: Session = Depends(get_db)):
    offer = Offer(**offer_create.dict())
    db.add(offer)
    db.commit()
    db.refresh(offer)


@offer_router.get("/{offer_id}", response_model=OfferDetailSchema)
async def detail_offer(offer_id: int, db: Session = Depends(get_db)):
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    return offer


@offer_router.put("/{offer_id}", response_model=OfferOutSchema)
async def update_offer(offer_id: int, offer_data: OfferUpdateSchema,
                       db: Session = Depends(get_db)):
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    for key, value in offer_data.dict().items():
        setattr(offer, key, value)
    db.commit()
    db.refresh(offer)
    return offer


@offer_router.delete("/{offer_id}")
async def delete_offer(offer_id: int, db: Session = Depends(get_db)):
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    db.delete(offer)
    db.commit()
    return {"message": "Offer deleted"}