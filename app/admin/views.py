from app.db.models import *
from sqladmin import ModelView


class UserProfileAdmin(ModelView, model=UserProfile):
    column_list = [UserProfile.first_name, UserProfile.last_name]


class SkillAdmin(ModelView, model=Skill):
    column_list = [Skill.skill_name]