from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.orm import declarative_base

from dotenv import load_dotenv

import os

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL").replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(
    DATABASE_URL,
    echo=False,          # flip to True when debugging specific SQL
    pool_pre_ping=True,  # safer pools
    hide_parameters=True # protects secrets if echo gets enabled
)



# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

Base = declarative_base()






