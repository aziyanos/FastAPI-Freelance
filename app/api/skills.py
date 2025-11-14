from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter
from typing import List
from app.db.database import SessionLocal
from app.db.schemas import (SkillOutSchema,
                            SkillCreateSchema,
                            SkillUpdateSchema)
from app.db.models import Skill


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


skill_router = APIRouter(prefix='/skill', tags=["Skills"])


@skill_router.post("/", response_model=SkillOutSchema)
def create_skills(skill_data: SkillCreateSchema,
                 db: Session = Depends(get_db)):
    new_skill = Skill(skill_name=skill_data.skill_name)
    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)
    return new_skill


@skill_router.get("/", response_model=List[SkillOutSchema])
async def list_skills(db: Session = Depends(get_db)):
    skill_db = db.query(Skill).all()
    return skill_db


@skill_router.get("/{skill_id}", response_model=SkillOutSchema)
async def detail_skills(skill_id: int, db: Session = Depends(get_db)):
    skill_db = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill_db:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill_db


@skill_router.put("/{skill_id}", response_model=SkillOutSchema)
async def update_skills(skill_data: SkillUpdateSchema, skill_id:int,
                       db: Session = Depends(get_db)):
    skill_db = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill_db:
        raise HTTPException(status_code=404, detail="Skill not found")
    skill_db.skill_name = skill_data.skill_name
    db.commit()
    db.refresh(skill_db)
    return skill_db


@skill_router.delete("/{skill_id}")
async def delete_skills(skill_id: int, db: Session = Depends(get_db)):
    skill_db = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill_db:
        raise HTTPException(status_code=404, detail="Skill not found")
    db.delete(skill_db)
    db.commit()
    return {"message": f"Skill {skill_id} deleted successfully"}




