from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends, HTTPException, APIRouter
from typing import List, AsyncGenerator
#from app.db.database import async_session_maker --> вынесли в отедльный файл deps
from app.db.schemas import (SkillOutSchema, SkillCreateSchema,
                            SkillUpdateSchema, SkillDetailSchema)
from app.db.models import Skill
from app.db.deps import get_db


skill_router = APIRouter(prefix='/skill', tags=["Skills"])


@skill_router.post("/", response_model=SkillOutSchema)
async def create_skill(skill_create: SkillCreateSchema,
                       db: AsyncSession = Depends(get_db)):
    new_skill = Skill(skill_name=skill_create.skill_name)
    db.add(new_skill)
    await db.flush()
    return new_skill


@skill_router.get("/", response_model=List[SkillOutSchema])
async def list_skills(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Skill))
    skill_db = result.scalars().all()
    return skill_db


@skill_router.get("/{skill_id}", response_model=SkillDetailSchema)
async def detail_skills(skill_id: int, db:
                    AsyncSession = Depends(get_db)):
    result = await db.execute(select(Skill).filter(Skill.id == skill_id))
    skill_db = result.scalar_one_or_none()
    if not skill_db:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill_db



@skill_router.put("/{skill_id}", response_model=SkillOutSchema)
async def update_skills(skill_data: SkillUpdateSchema, skill_id:int,
                       db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Skill).filter(Skill.id == skill_id))
    skill_db = result.scalar_one_or_none()
    if not skill_db:
        raise HTTPException(status_code=404, detail="Skill not found")
    #exclude_unset=True возвращает только те поля, которые клиент отправил.
    for key, value in skill_data.dict(exclude_unset=True).items():
        setattr(skill_db, key, value)
    await db.flush()
    return skill_db


@skill_router.delete("/{skill_id}")
async def delete_skills(skill_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Skill).filter(Skill.id == skill_id))
    skill_db = result.scalars().one_or_none()
    if not skill_db:
        raise HTTPException(status_code=404, detail="Skill not found")
    await db.delete(skill_db)
    await db.flush()
    return {"message": f"Skill {skill_id} deleted successfully"}




