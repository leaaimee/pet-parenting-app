from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pycparser.ply.yacc import resultlimit

from sqlalchemy.future import select
from sqlalchemy.util import await_only

from backend.models.users_models import Users
from sqlalchemy.ext.asyncio import AsyncSession
from backend.schemas.user_schema import UserProfileShowSchema
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
from backend.schemas.user_schema import UserProfileShowSchema

async def get_user(email: str, session: AsyncSession):
    try:
        result = await session.execute(select(Users).where(Users.email == email))
        user_from_db = result.scalar_one_or_none()  # Awaited the result
        print("--------------")
        print(user_from_db)  # Print the user object
        print("--------------")
        if user_from_db:
            return UserProfileShowSchema.from_orm(user_from_db)  # Use from_orm for Pydantic schema validation
        else:
            return None  # Explicitly return None if no user is found
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Now implementing


async def authenticate_user(email: str, password: str, session: AsyncSession):
    result = await session.execute(select(Users).where(Users.email == email))
    user = result.scalar_one_or_none()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await session.execute(select(Users).where(Users.email == email))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user
