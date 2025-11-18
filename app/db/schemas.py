from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional
from app.db.models import RoleChoices, StatusChoices
from datetime import datetime, date
from decimal import Decimal
from pydantic import field_validator
import re


#////////////////////////////////////////////////////
class SkillSchemaBase(BaseModel):
#Базовая схема
    skill_name: str = Field(min_length=1, max_length=250)

class SkillCreateSchema(SkillSchemaBase):
    ...

class SkillDetailSchema(SkillSchemaBase):
    id: int
    ...

class SkillUpdateSchema(BaseModel):
    skill_name: Optional[str] = Field(None, min_length=1, max_length=250)
    # Можно отправить пустое тело, если ничего не меняем

class SkillOutSchema(SkillSchemaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)  # Новый синтаксис Pydantic v2


#////////////////////////////////////////////////////
class UserProfileBaseSchema(BaseModel):
    first_name: str = Field(... ,min_length=1, max_length=100)
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

    @field_validator('password')
    def validate_password(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain uppercase')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain lowercase')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain digit')
        return v


class UserProfileDetailSchema(UserProfileBaseSchema):
    id: int
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

class UserProfileRegisterSchema(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    user_name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=5, max_length=72)
    age: Optional[int] = Field(None, gt=0, lt=100)
    phone_number: Optional[str] = None
    role: RoleChoices
    avatar: Optional[str] = Field(None, min_length=1, max_length=250)

    @field_validator('password')
    def validate_password(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain uppercase')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain lowercase')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain digit')
        return v

class UserProfileLoginSchema(BaseModel):
    user_name: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1, max_length=72)

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
    id: int
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
    id: int
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
    id: int
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
    id: int
    pass

class ReviewUpdateSchema(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = Field(None, min_length=5, max_length=2000)

class ReviewOutSchema(ReviewBaseSchema):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

