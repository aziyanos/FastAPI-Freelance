from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter
from typing import List
from app.db.database import SessionLocal
from app.db.schemas import (ProjectOutSchema, ProjectCreateSchema,
                            ProjectUpdateSchema, ProjectDetailSchema)
from app.db.models import Project


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


project_router = APIRouter(prefix="/project", tags=["Projects"])


@project_router.get("/", response_model=List[ProjectOutSchema])
async def list_project(db: Session = Depends(get_db)):
    project_db = db.query(Project).all()
    return project_db


@project_router.post("/", response_model=ProjectOutSchema)
async def create_project(project_data: ProjectCreateSchema,
                         db: Session = Depends(get_db)):
    new_project = Project(**project_data.dict())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


@project_router.get("/{project_id}", response_model=ProjectDetailSchema)
async def detail_project(project_id: int, db: Session
                                        = Depends(get_db)):
    project_db = db.query(Project).filter(Project.id == project_id).first()
    if not project_db:
        raise HTTPException(status_code=404, detail="Project not found")
    return project_db


@project_router.put("/{project_id}", response_model=ProjectOutSchema)
async def update_project(project_id: int, project_data: ProjectUpdateSchema,
                         db: Session = Depends(get_db)):
    project_db = db.query(Project).filter(Project.id == project_id).first()
    if not project_db:
        raise HTTPException(status_code=404, detail="Project not found")
    #обновить существующую запись к новым значением
    for key, value in project_data.dict(exclude_unset=True).items():
        setattr(project_db, key, value)
    db.commit()
    db.refresh(project_db)
    return project_db


@project_router.delete("/{project_id}")
async def delete_project(project_id: int,
                         db: Session = Depends(get_db)):
    project_db = db.query(Project).filter(Project.id == project_id).first()
    if not project_db:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project_db)
    db.commit()
    return {"message": "Project deleted"}

