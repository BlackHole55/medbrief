from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from contextlib import asynccontextmanager

from app.config import settings

async_engine = create_async_engine(
    settings.POSTGRES_DSN,
    pool_pre_ping=True, # Checks connection liveness before running queries
    echo=True, # Raw SQL queries printed in logs
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

@asynccontextmanager
async def get_worker_db() -> AsyncGenerator[AsyncSession, None]:
    """
    A context manager that provides an isolated database session 
    for background workers and non-FastAPI scripts.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()