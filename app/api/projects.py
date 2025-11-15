from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends, HTTPException, APIRouter, Response, status
from typing import List, AsyncGenerator
from app.db.database import async_session_maker
from app.db.schemas import (ProjectOutSchema, ProjectCreateSchema,
                            ProjectUpdateSchema, ProjectDetailSchema)
from app.db.models import Project
from app.db.deps import get_db


project_router = APIRouter(prefix="/project", tags=["Projects"])


@project_router.get("/", response_model=List[ProjectOutSchema])
async def list_project(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project))
    project_db = result.scalars().all()
    return project_db


@project_router.post("/", response_model=ProjectOutSchema)
async def create_project(project_create: ProjectCreateSchema,
                         db: AsyncSession = Depends(get_db)):
    new_project = Project(**project_create.model_dump())
    db.add(new_project)
    await db.flush()
    return new_project


@project_router.get("/{project_id}", response_model=ProjectDetailSchema)
async def detail_project(project_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project).filter(Project.id == project_id))
    project_db = result.scalar_one_or_none()
    if not project_db:
        raise HTTPException(status_code=404, detail="Project not found")
    return project_db


@project_router.put("/{project_id}", response_model=ProjectOutSchema)
async def update_project(project_id: int, project_data: ProjectUpdateSchema,
                         db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project).filter(Project.id == project_id))
    project_db = result.scalar_one_or_none()
    if not project_db:
        raise HTTPException(status_code=404, detail="Project not found")

    # обновить существующую запись к новым значением
    for key, value in project_data.dict(exclude_unset=True).items():
        setattr(project_db, key, value)

    await db.flush()
    await db.refresh(project_db)
    return project_db


@project_router.delete("/{project_id}")
async def delete_project(project_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project).filter(Project.id == project_id))
    project_db = result.scalar_one_or_none()
    if not project_db:
        raise HTTPException(status_code=404, detail="Project not found")

    await db.delete(project_db)
    await db.flush()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

