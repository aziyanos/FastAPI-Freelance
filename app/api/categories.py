from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends, HTTPException, APIRouter
from typing import List, AsyncGenerator
from app.db.database import async_session_maker
from app.db.schemas import (CategoryOutSchema, CategoryCreateSchema,
                            CategoryDetailSchema, CategoryUpdateSchema)
from app.db.models import Category
from app.db.deps import get_db


category_router = APIRouter(prefix="/category", tags=["Categories"])


@category_router.get("/", response_model=List[CategoryOutSchema])
async def list_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category))
    category_db = result.scalars().all()
    return category_db


@category_router.post("/", response_model=CategoryOutSchema)
async def create_categories(category_create: CategoryCreateSchema,
                            db: AsyncSession = Depends(get_db)):
    new_category= Category(category_name=category_create.category_name)
    db.add(new_category)
    await db.flush() #Получаем id от БД
    #await db.refresh(new_category)  # ← Добавить, если есть server_default, datetime
    return new_category #Автоматический commit через session.begin()


@category_router.get("/{category_id}", response_model=CategoryDetailSchema)
async def detail_categories(category_id: int, db:
                            AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).filter(Category.id == category_id))
    category_db = result.scalar_one_or_none()
    if not category_db:
        raise HTTPException(status_code=404, detail="Category not found")
    return category_db


@category_router.put("/{category_id}", response_model=CategoryOutSchema)
async def update_categories(category_id: int, category_data: CategoryUpdateSchema,
                            db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).filter(Category.id == category_id))
    category_db = result.scalar_one_or_none()
    if not category_db:
        raise HTTPException(status_code=404, detail="Category not found")
    #обновление значения поля существующего объекта SQLAlchemy (category_db)
    # новым значением, полученным из Pydantic-схемы (category_data).
    category_db.category_name = category_data.category_name
    await db.flush()
    return category_db


@category_router.delete("/{category_id}")
async def delete_categories(category_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category).filter(Category.id == category_id))
    category_db = result.scalar_one_or_none()
    if not category_db:
        raise HTTPException(status_code=404, detail="Category not found")
    await db.delete(category_db)
    await db.flush()
    return {"message": "Category deleted"}
