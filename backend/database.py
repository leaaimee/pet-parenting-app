from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.orm import declarative_base

from dotenv import load_dotenv

import os

load_dotenv()


# Pull your database URL from .env
DATABASE_URL = os.getenv("DATABASE_URL").replace("postgresql://", "postgresql+asyncpg://")

#  Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)


# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# 🧪 Use in routes/services
# go
# async def get_async_session():
#     async with AsyncSessionLocal() as session:
#         yield session

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

# Base class for your models to inherit
Base = declarative_base()




# from contextlib import contextmanager
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker


# Load from .env or config - sync flow
# DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine - sync version
# engine = create_engine(DATABASE_URL)

# Create session factory (used for making db sessions)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# sync version
# @contextmanager
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()






