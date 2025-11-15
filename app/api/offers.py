from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from typing import List, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.database import async_session_maker
from app.db.schemas import (OfferOutSchema, OfferCreateSchema,
                            OfferUpdateSchema, OfferDetailSchema)
from app.db.models import Offer


#Используйте flush() в endpoints, а не refresh()
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        async with session.begin():
            yield session


offer_router = APIRouter(prefix="/offers", tags=["Offers"])


@offer_router.get("/", response_model=List[OfferOutSchema])
async def list_offers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Offer))
    offers_db = result.scalars().all()
    return offers_db


@offer_router.post("/", response_model=OfferOutSchema)
async def create_offer(offer_create: OfferCreateSchema,
                       db: AsyncSession = Depends(get_db)):
    new_offer = Offer(**offer_create.dict())
    db.add(new_offer)
    await db.flush()
    return new_offer


@offer_router.get("/{offer_id}", response_model=OfferDetailSchema)
async def detail_offer(offer_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Offer).filter(Offer.id == offer_id))
    offer_db = result.scalar_one_or_none()
    if not offer_db:
        raise HTTPException(status_code=404, detail="Offer not found")
    return offer_db


@offer_router.put("/{offer_id}", response_model=OfferOutSchema)
async def update_offer(offer_id: int, offer_data: OfferUpdateSchema,
                       db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Offer).filter(Offer.id == offer_id))
    offer_db = result.scalar_one_or_none()
    if not offer_db:
        raise HTTPException(status_code=404, detail="Offer not found")
    for key, value in offer_data.dict(exclude_unset=True).items():
        setattr(offer_db, key, value)
    await db.flush()
    await db.flush()
    return offer_db


@offer_router.delete("/{offer_id}")
async def delete_offer(offer_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Offer).filter(Offer.id == offer_id))
    offer_db = result.scalar_one_or_none()
    if not offer_db:
        raise HTTPException(status_code=404, detail="Offer not found")
    await db.delete(offer_db)
    await db.flush()
    return {"message": "Offer deleted"}