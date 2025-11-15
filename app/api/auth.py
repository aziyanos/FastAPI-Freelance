from fastapi import HTTPException, Depends, APIRouter
from app.db.models import UserProfile, RefreshToken
from app.db.schemas import (UserProfileOutSchema, UserProfileLoginSchema,
                            UserProfileCreateSchema, UserProfileUpdateSchema, UserProfileRegisterSchema)
from app.db.database import async_session_maker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from app.config import (ALGORITHM, SECRET_KEY,
                        ACCESS_TOKEN_LIFETIME,
                        REFRESH_TOKEN_LIFETIME)
from datetime import datetime, timedelta
from app.encription import encrypt_data, decrypt_data
from typing import AsyncGenerator
import hashlib
import base64
import bcrypt
from app.config import *
#без passlib, прямой bcrypt

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        async with session.begin():
            yield session


auth_router = APIRouter(prefix='/auth', tags=['Auth'])



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля с использованием bcrypt напрямую"""
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8') if isinstance(hashed_password, str) else hashed_password
    )


def get_password_hash(password: str) -> str:
    """Хеширование пароля с использованием bcrypt напрямую"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Создание access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_LIFETIME))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict) -> str:
    """Создание refresh token"""
    return create_access_token(data, expires_delta=timedelta(days=REFRESH_TOKEN_LIFETIME))


@auth_router.post('/register', response_model=dict)
async def register(user:UserProfileRegisterSchema, db:AsyncSession = Depends(get_db)):
    # Проверка существования username
    result = await db.execute(
        select(UserProfile).filter(UserProfile.user_name == user.user_name)
    )
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="user_name уже существует")

        # Шифруем email и телефон
    #encrypted_email = encrypt_data(user.email)
    #encrypted_phone = encrypt_data(user.phone_number) if user.phone_number else None

        # Проверка существования email
    #result = await db.execute(
     #  select(UserProfile).filter(UserProfile.email == encrypted_email)
       # )
    #if result.scalars().first():
     #   raise HTTPException(status_code=400, detail="email уже существует")


    hash_password = get_password_hash(user.password)

    # Создаем пользователя
    user_db = UserProfile(
        first_name=user.first_name,
        last_name=user.last_name,
        user_name=user.user_name,
        email=user.email,
        age=user.age,
        phone_number=user.phone_number,
        role=user.role,
        password=hash_password
    )

    db.add(user_db)
    await db.flush()

    return {"message": "Вы успешно зарегистрировались", "user_id": user_db.id}


@auth_router.post('/login')
async def login(form_data: UserProfileLoginSchema, db: AsyncSession = Depends(get_db)):
    """Вход пользователя"""

    # Поиск пользователя
    result = await db.execute(
        select(UserProfile).filter(UserProfile.user_name == form_data.user_name)
    )
    user = result.scalars().first()

    # Проверка пользователя и пароля
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail='Данные логина неправильные')

    # Создание токенов
    access_token = create_access_token({"sub": user.user_name})
    refresh_token = create_refresh_token({"sub": user.user_name})

    # Сохранение refresh token
    new_token = RefreshToken(user_id=user.id, token=refresh_token)
    db.add(new_token)
    await db.flush()

    # Дешифруем данные перед отправкой клиенту

    #decrypted_email = decrypt_data(user.email) if user.email else None
    #decrypted_phone = decrypt_data(user.phone_number) if user.phone_number else None

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        #"user_info": {
         #   "user_name": user.user_name,
         #   "email": decrypted_email,  # Возвращаем дешифрованный email
          #  "phone_number": decrypted_phone  # Возвращаем дешифрованный телефон
        #}
    }


@auth_router.post('/logout')
async def logout(refresh_token: str, db: AsyncSession = Depends(get_db)):
    """Выход пользователя"""

    # Поиск токена
    result = await db.execute(
        select(RefreshToken).filter(RefreshToken.token == refresh_token)
    )
    stored_token = result.scalars().first()

    if not stored_token:
        raise HTTPException(status_code=401, detail='Токен не найден')

    # Удаление токена
    await db.delete(stored_token)
    await db.commit()

    return {"message": "Вы успешно вышли"}


@auth_router.post('/refresh')
async def refresh(refresh_token: str, db: AsyncSession = Depends(get_db)):
    """Обновление access token"""

    # Поиск refresh token
    result = await db.execute(
        select(RefreshToken).filter(RefreshToken.token == refresh_token)
    )
    stored_token = result.scalars().first()

    if not stored_token:
        raise HTTPException(status_code=401, detail='Токен не найден или истек')

    # Получение пользователя
    result = await db.execute(
        select(UserProfile).filter(UserProfile.id == stored_token.user_id)
    )
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=401, detail='Пользователь не найден')

    # Создание нового access token
    access_token = create_access_token({"sub": user.user_name})

    return {"access_token": access_token, "token_type": "bearer"}

