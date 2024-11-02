from typing import AsyncGenerator

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

async_engine: AsyncEngine = create_async_engine(
    settings.POSTGRES_ASYNC_URI, echo=False, future=True
)


local_session = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)  # type: ignore


async def async_get_db() -> AsyncGenerator[AsyncSession, None]:
    async_session = local_session

    async with async_session() as db:
        yield db
        await db.commit()
