from decimal import Decimal
from app.db.database import Base
from fastapi import FastAPI
from sqlalchemy import Integer, String, Enum, DateTime, Text, ForeignKey, DECIMAL, Table, Column, func, CheckConstraint
from sqlalchemy.orm import Mapped, relationship, mapped_column
from enum import Enum as PyEnum
from typing import Optional, List
from datetime import datetime


#для manytomany, Отедельная БД таблица для Skill_project
skill_project = Table(
    'skill_project',
    Base.metadata,
    Column('project_id', ForeignKey('projects.id', ondelete='CASCADE'), primary_key=True),
    Column('skill_id', ForeignKey('skills.id', ondelete='CASCADE'), primary_key=True)
)

user_skill = Table(
    'user_skill',
    Base.metadata,
    Column('user_id', ForeignKey('userprofiles.id', ondelete='CASCADE'), primary_key=True),
    Column('skill_id', ForeignKey('skills.id', ondelete='CASCADE'), primary_key=True)
)

#////////////////////////////////////////////////////////////////////
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
                                                             secondary=user_skill,
                                                             lazy="selectin")

    # Проекты, требующие этот навык
    project_skills: Mapped[List['Project']] = relationship("Project",
                                                           secondary=skill_project,
                                                           back_populates='skill_required',
                                                           lazy="selectin")

    def __repr__(self):
        return f"<Skill {self.skill_name}>"


class UserProfile(Base):
    __tablename__ = "userprofiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    user_name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(1000), unique=True, index=True)
    age:Mapped[Optional[int]] = mapped_column(Integer)
    phone_number: Mapped[Optional[str]] = mapped_column(String(1000))
    role: Mapped[RoleChoices] = mapped_column(Enum(RoleChoices), default=RoleChoices.client)
    biography: Mapped[Optional[str]] = mapped_column(Text)
    avatar: Mapped[Optional[str]] = mapped_column(String(250))
    password: Mapped[str] = mapped_column(String(1000))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


    #Клиенты могут регистрироваться без навыков, так как без optional не могут зарегистрироваться
    skill: Mapped[List[Skill]] = relationship('Skill', back_populates="user_profiles",
                                                                secondary=user_skill, lazy="selectin")

    # Проекты, созданные пользователем (если клиент)
    projects: Mapped[List['Project']] = relationship("Project", back_populates="client",
                                                     cascade='all, delete-orphan',lazy="selectin"
                                                     )

    # Предложения, сделанные фрилансером
    offers: Mapped[List['Offer']] = relationship("Offer", back_populates="freelancer",
                                                 cascade='all, delete-orphan', lazy="selectin")

    # Отзывы, оставленные этим пользователем
    given_reviews: Mapped[List['Review']] = relationship('Review', back_populates="reviewer",
                                                         foreign_keys='Review.reviewer_id',
                                                         cascade='all, delete-orphan',lazy="selectin")

    # Отзывы, полученные этим пользователем
    received_reviews: Mapped[List['Review']] = relationship('Review', back_populates="target",
                                                            foreign_keys='Review.target_id',
                                                            cascade='all, delete-orphan',lazy="selectin")

    refresh_tokens: Mapped[List['RefreshToken']] = relationship('RefreshToken', back_populates='user',
                                                                cascade='all, delete-orphan',lazy="selectin")

    def __repr__(self):
        return f"<UserProfile {self.first_name} {self.last_name}>"


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_name: Mapped[str] = mapped_column(String(32), index=True)

    projects: Mapped[List['Project']] = relationship("Project", back_populates="category",
                                                                                    lazy="selectin")
               #Убран cascade projects: (не удаляем проекты при удалении категории)

    def __repr__(self):
        return f"<Category {self.category_name}>"


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_name: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    budget: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(12,2))
    deadline: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[StatusChoices] = mapped_column(Enum(StatusChoices), default=StatusChoices.open)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime,default=func.now(), onupdate=func.now())


    # Категория проекта.  --> lazy='joined'
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"), index=True)
    category: Mapped[Category] = relationship('Category', back_populates="projects",lazy="joined")


    # Клиент, создавший проект
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey("userprofiles.id"), index=True)
    client: Mapped[UserProfile] = relationship("UserProfile", back_populates="projects",lazy="selectin")


    # manytomany убран skill_id, так как это many-to-many
    skill_required: Mapped[List[Skill]] = relationship("Skill", secondary=skill_project,
                                                back_populates="project_skills",
                                                       lazy="selectin")
    # Предложения на проект
    offers: Mapped[List['Offer']] = relationship("Offer", back_populates="project",
                                                 cascade='all, delete-orphan',lazy="selectin")

    # Отзывы по проекту
    project_reviews: Mapped[List['Review']] = relationship("Review", back_populates="project",
                                                           cascade='all, delete-orphan',lazy="selectin")

    def __repr__(self):
        return f"<Project {self.project_name}>"


class Offer(Base):
    __tablename__ = "offers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    message: Mapped[str] = mapped_column(Text)
    proposed_budget: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(12,2))
    proposed_deadline: Mapped[Optional[datetime]] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    # Проект, на который сделано предложение
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"), index=True)
    project: Mapped[Project] = relationship("Project", back_populates="offers",lazy="selectin")

    # Фрилансер, сделавший предложение
    freelancer_id: Mapped[int] = mapped_column(Integer, ForeignKey("userprofiles.id"), index=True)
    freelancer: Mapped[UserProfile] = relationship("UserProfile", back_populates="offers",
                                                                                    lazy="selectin")

    def __repr__(self):
        return f"<Offer {self.message}>"


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    rating: Mapped[Optional[int]] = mapped_column(Integer, CheckConstraint("rating >= 1 AND rating <= 5"))
    comment: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    # Проект, по которому оставлен отзыв
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"), index=True)
    project: Mapped[Project] = relationship("Project", back_populates="project_reviews",lazy="selectin")

    # Кто оставил отзыв
    reviewer_id: Mapped[int] = mapped_column(Integer, ForeignKey("userprofiles.id"), index=True)
    reviewer: Mapped[UserProfile] = relationship("UserProfile", back_populates="given_reviews",
                                                 foreign_keys=[reviewer_id], lazy="selectin")

    # О ком отзыв
    target_id: Mapped[int] = mapped_column(Integer, ForeignKey("userprofiles.id"), index=True)
    target: Mapped[UserProfile] = relationship("UserProfile", back_populates="received_reviews",
                                               foreign_keys=[target_id], lazy="selectin")

    def __repr__(self):
        return f"<Review {self.rating}>"


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("userprofiles.id"), index=True)
    user: Mapped[UserProfile] = relationship("UserProfile", back_populates="refresh_tokens",
                                                                        lazy = "selectin"
                                             )
    token: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())




 #uselist=False,  # ← КЛЮЧЕВОЕ отличие от One-to-Many






