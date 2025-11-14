from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.db.database import SessionLocal
from app.db.schemas import (CategoryOutSchema, CategoryCreateSchema,
                            CategoryDetailSchema, CategoryUpdateSchema)
from app.db.schemas import Category


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


category_router = APIRouter(prefix="/category", tags=["Categories"])


@category_router.get("/", response_model=List[CategoryOutSchema])
async def list_categories(
                          db: Session = Depends(get_db)):
    category_db = db.query(Category).all()
    return category_db


@category_router.post("/", response_model=CategoryOutSchema)
async def create_categories(category_data: CategoryCreateSchema,
                            db: Session = Depends(get_db)):
    new_category= Category(category_name=category_data.category_name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@category_router.get("/{category_id}", response_model=CategoryDetailSchema)
async def detail_categories(category_id: int, db:
                            Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if not category_db:
        raise HTTPException(status_code=404, detail="Category not found")
    return category_db


@category_router.put("/{category_id}", response_model=CategoryOutSchema)
async def update_categories(category_id: int, category_data: CategoryUpdateSchema,
                            db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if not category_db:
        raise HTTPException(status_code=404, detail="Category not found")
    #обновление значения поля существующего объекта SQLAlchemy (category_db)
    # новым значением, полученным из Pydantic-схемы (category_data).
    category_db.category_name = category_data.category_name
    db.commit()
    db.refresh(category_db)
    return category_db


@category_router.delete("/{category_id}")
async def delete_categories(category_id: int, db: Session = Depends(get_db)):
    category_db = db.query(Category).filter(Category.id == category_id).first()
    if not category_db:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category_db)
    db.commit()
    return {"message": "Category deleted"}
