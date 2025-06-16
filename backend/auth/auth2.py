from datetime import datetime, timedelta
from sys import exception
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from passlib.context import CryptContext

from backend.database import get_async_session

from jose import JWTError, jwt
from dotenv import load_dotenv
import os

load_dotenv()


# 🔐 Security config
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Password hashing - by Charles
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Token scheme for protected routes - by Charles
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



# base verify - by Charles
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# get pw verify - by Charles
def get_password_hash(password):
    return pwd_context.hash(password)


from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.users_models import Users
from backend.schemas.user_schema import UserPublic, TokenData

# Charles Version
# async def get_user(email: str, session: AsyncSession):
#     try:
#         result = await session.execute(select(Users).where(Users.email == email))
#         user_from_db = result.scalar_one_or_none()  # Awaited the result
#         if user_from_db:
#             return UserPublic.from_orm(user_from_db)  # Use from_orm for Pydantic schema validation
#         else:
#             return None  # Explicitly return None if no user is found
#     except Exception as e:
#         return e

# chatgpt version

from fastapi import HTTPException
from backend.schemas.user_schema import UserAccountShowSchema
from backend.models.users_models import Users
from sqlalchemy import select

async def get_user(email: str, session: AsyncSession):
    try:
        result = await session.execute(select(Users).where(Users.email == email))
        user = result.scalar_one_or_none()
        if user:
            return UserAccountShowSchema.from_orm(user)
        return None
    except Exception as e:
        print("❌ get_user error:", e)
        raise HTTPException(status_code=500, detail="Error accessing user")





# Dominiks version
# async def get_user(email: str, session: AsyncSession):
#     print("EIN ZEICHEN!")
#     try:
#         result = await session.execute(select(Users).where(Users.email == email))
#         user_from_db = result.scalar_one_or_none()  # Awaited the result
#         print("USER FROM DB:", user_from_db)
#         if user_from_db:
#             return UserPublic.model_validate(user_from_db)
#         else:
#             return None  # Explicitly return None if no user is found
#     except Exception as e:
#         raise Exception("unknown Error:", e)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await session.execute(select(Users).where(Users.email == email))
    user = result.scalar_one_or_none()
    if not user:
        raise credentials_exception

    return user

# Now implementing

async def authenticate_user(username: str, password: str, session: AsyncSession = Depends(get_async_session)):
    user = await get_user(session, username)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user



def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(email: str, session: AsyncSession, token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user(email, session)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[Users, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user