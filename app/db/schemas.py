from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional
from app.db.models import RoleChoices, StatusChoices
from datetime import datetime, date
from decimal import Decimal


#////////////////////////////////////////////////////
class SkillSchemaBase(BaseModel):
#Базовая схема
    skill_name: str = Field(min_length=1, max_length=250)

class SkillCreateSchema(SkillSchemaBase):
    pass

class SkillUpdateSchema(BaseModel):
    skill_name: Optional[str] = Field(None, min_length=1, max_length=250)
    # Можно отправить пустое тело, если ничего не меняем

class SkillOutSchema(SkillSchemaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)  # Новый синтаксис Pydantic v2


#////////////////////////////////////////////////////
class UserProfileBaseSchema(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    user_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: Optional[int] = Field(None, gt=0, lt=100)
    phone_number: Optional[str] = None
    role: RoleChoices
    biography: Optional[str] = Field(None, min_length=5, max_length=2000)
    avatar: Optional[str] = Field(None, min_length=1, max_length=250)

class UserProfileCreateSchema(UserProfileBaseSchema):
    password: str = Field(min_length=5, max_length=100)

class UserProfileDetailSchema(UserProfileBaseSchema):
    pass

class UserProfileUpdateSchema(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    user_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, gt=0, lt=100)
    phone_number: Optional[str] = None
    role: Optional[RoleChoices] = None
    biography: Optional[str] = Field(None, min_length=5, max_length=2000)
    avatar: Optional[str] = Field(None, max_length=250)
    password: Optional[str] = Field(None, min_length=8)

class UserProfileOutSchema(UserProfileBaseSchema):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


#////////////////////////////////////////////////////
class CategoryBaseSchema(BaseModel):
    category_name: str = Field(min_length=1, max_length=250)

class CategoryCreateSchema(CategoryBaseSchema):
    pass

class CategoryUpdateSchema(CategoryBaseSchema):
    pass

class CategoryDetailSchema(CategoryBaseSchema):
    pass

class CategoryOutSchema(CategoryBaseSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)


#////////////////////////////////////////////////////
class ProjectBaseSchema(BaseModel):
    project_name: str
    category_id: int = Field(gt=0) #Использование Field(...) для обязательных полей
    client_id: Optional[int] = None
    description: Optional[str] = Field(None, min_length=5, max_length=2000)
    budget: Optional[Decimal] = Field(None, decimal_places=2, max_digits=12)
    deadline: Optional[datetime] = None
    status: StatusChoices

class ProjectCreateSchema(ProjectBaseSchema):
    pass

class ProjectUpdateSchema(BaseModel):
    project_name: Optional[str] = None
    category_id: Optional[int] = Field(None, gt=0)
    client_id: Optional[int] = None
    description: Optional[str] = Field(None, min_length=5, max_length=2000)
    budget: Optional[Decimal] = Field(None, decimal_places=2, max_digits=12)
    deadline: Optional[datetime] = None
    status: Optional[StatusChoices] = None

class ProjectDetailSchema(ProjectBaseSchema):
    pass

class ProjectOutSchema(ProjectBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


#////////////////////////////////////////////////////
class OfferBaseSchema(BaseModel):
    message: str = Field(min_length=5, max_length=2000)
    proposed_budget: Decimal = Field(decimal_places=2, max_digits=12)
    proposed_deadline: datetime
    project_id: int = Field(gt=0)
    freelancer_id: int = Field(gt=0)

class OfferCreateSchema(OfferBaseSchema):
    pass

class OfferDetailSchema(OfferBaseSchema):
    pass

class OfferUpdateSchema(BaseModel):
    message: Optional[str] = Field(None, min_length=5, max_length=2000)
    proposed_budget: Optional[Decimal] = Field(None, decimal_places=2, max_digits=12)
    proposed_deadline: Optional[datetime] = None
    #project_id: int = Field(gt=0) если хотим менять project_id
    #freelancer_id: int = Field(gt=0) если хотим менять freelancer_id

class OfferOutSchema(OfferBaseSchema):
    id: int
    created_at: datetime  # БД генерирует автоматическии, не нужно для базавой схеме
    model_config = ConfigDict(from_attributes=True)


#////////////////////////////////////////////////////
class ReviewBaseSchema(BaseModel):
    rating: Optional[int] = Field(ge=1, le=5)
    comment: Optional[str] = Field(None, min_length=5, max_length=2000)
    project_id: int = Field(gt=0)
    reviewer_id: int = Field(gt=0)
    target_id: int = Field(gt=0)

class ReviewCreateSchema(ReviewBaseSchema):
    pass

class ReviewDetailSchema(ReviewBaseSchema):
    pass

class ReviewUpdateSchema(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = Field(None, min_length=5, max_length=2000)

class ReviewOutSchema(ReviewBaseSchema):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

