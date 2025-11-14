from decimal import Decimal
from app.db.database import Base
from fastapi import FastAPI
from sqlalchemy import Integer, String, Enum, DateTime, Text, ForeignKey, DECIMAL, Table, Column, func, CheckConstraint
from sqlalchemy.orm import Mapped, relationship, mapped_column
from enum import Enum as PyEnum
from typing import Optional, List
from datetime import datetime


#для manytomany, Промежуточная таблица для Skill
skill_project = Table(
    'skill_project',
    Base.metadata,
    Column('project_id', ForeignKey('projects.id'), primary_key=True),
    Column('skill_id', ForeignKey('skills.id'), primary_key=True)
)


class RoleChoices(str, PyEnum):
    admin = "admin"
    client = "client"
    freelancer = "freelancer"


class StatusChoices(str, PyEnum):
    open = "open"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


class Skill(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    skill_name: Mapped[str] = mapped_column(String(100), index=True)

    # Фрилансеры, обладающие этим навыком
    user_profiles:Mapped[List['UserProfile']] = relationship("UserProfile",
                                                            back_populates="skill",
                                                            cascade="all, delete-orphan")

    # Проекты, требующие этот навык
    project_skills: Mapped[List['Project']] = relationship("Project",
                                                           secondary=skill_project,
                                                           back_populates='skill_required')



class UserProfile(Base):
    __tablename__ = "userprofiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    user_name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    age:Mapped[Optional[int]] = mapped_column(Integer)
    phone_number: Mapped[Optional[str]] = mapped_column(String(25))
    role: Mapped[RoleChoices] = mapped_column(Enum(RoleChoices), default=RoleChoices.client)
    biography: Mapped[Optional[str]] = mapped_column(Text)
    avatar: Mapped[Optional[str]] = mapped_column(String(250))
    password: Mapped[str] = mapped_column(String(250))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    skill_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("skills.id"), index=True)
    #Клиенты могут регистрироваться без навыков, так как без optional не могут зарегистрироваться
    skill: Mapped[Optional[Skill]] = relationship('Skill', back_populates="user_profiles")

    # Проекты, созданные пользователем (если клиент)
    projects: Mapped[List['Project']] = relationship("Project", back_populates="client",
                                                     cascade='all, delete-orphan')

    # Предложения, сделанные фрилансером
    offers: Mapped[List['Offer']] = relationship("Offer", back_populates="freelancer",
                                                 cascade='all, delete-orphan')

    # Отзывы, оставленные этим пользователем
    given_reviews: Mapped[List['Review']] = relationship('Review', back_populates="reviewer",
                                                         foreign_keys='Review.reviewer_id',
                                                         cascade='all, delete-orphan')

    # Отзывы, полученные этим пользователем
    received_reviews: Mapped[List['Review']] = relationship('Review', back_populates="target",
                                                            foreign_keys='Review.target_id',
                                                            cascade='all, delete-orphan')




class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(String(32), index=True)

    projects: Mapped[List['Project']] = relationship("Project", back_populates="category",
                                                     cascade="all, delete-orphan")


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_name: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    budget: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(12,2))
    deadline: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[StatusChoices] = mapped_column(Enum(StatusChoices), default=StatusChoices.open)
    created_at: Mapped[datetime] = mapped_column(DateTime,server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime,server_default=func.now(), onupdate=func.now())


    # Категория проекта
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"), index=True)
    category: Mapped[Category] = relationship('Category', back_populates="projects")


    # Клиент, создавший проект
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey("userprofiles.id"), index=True)
    client: Mapped[UserProfile] = relationship("UserProfile", back_populates="projects")


    # manytomany убран skill_id, так как это many-to-many
    skill_required: Mapped[List[Skill]] = relationship("Skill", secondary=skill_project,

                                                back_populates="project_skills")
    # Предложения на проект
    offers: Mapped[List['Offer']] = relationship("Offer", back_populates="project",
                                                 cascade='all, delete-orphan')

    # Отзывы по проекту
    project_reviews: Mapped[List['Review']] = relationship("Review", back_populates="project",
                                                           cascade='all, delete-orphan')


class Offer(Base):
    __tablename__ = "offers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    message: Mapped[str] = mapped_column(Text)
    proposed_budget: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(12,2))
    proposed_deadline: Mapped[Optional[datetime]] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Проект, на который сделано предложение
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"), index=True)
    project: Mapped[Project] = relationship("Project", back_populates="offers")

    # Фрилансер, сделавший предложение
    freelancer_id: Mapped[int] = mapped_column(Integer, ForeignKey("userprofiles.id"), index=True)
    freelancer: Mapped[UserProfile] = relationship("UserProfile", back_populates="offers")


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    rating: Mapped[Optional[int]] = mapped_column(Integer, CheckConstraint("rating >= 1 AND rating <= 5"))
    comment: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Проект, по которому оставлен отзыв
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"), index=True)
    project: Mapped[Project] = relationship("Project", back_populates="project_reviews")

    # Кто оставил отзыв
    reviewer_id: Mapped[int] = mapped_column(Integer, ForeignKey("userprofiles.id"), index=True)
    reviewer: Mapped[UserProfile] = relationship("UserProfile", back_populates="given_reviews",
                                                 foreign_keys=[reviewer_id])

    # О ком отзыв
    target_id: Mapped[int] = mapped_column(Integer, ForeignKey("userprofiles.id"), index=True)
    target: Mapped[UserProfile] = relationship("UserProfile", back_populates="received_reviews",
                                               foreign_keys=[target_id])












