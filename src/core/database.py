import logging
import contextlib

from typing import AsyncIterator, Optional

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext import asyncio


logger = logging.getLogger(__name__)

Base = declarative_base()


class DatabaseSessionManager:
    def __init__(self) -> None:
        self._engine: Optional[asyncio.AsyncEngine] = None
        self._sessionmaker: Optional[asyncio.async_sessionmaker[asyncio.AsyncSession]] = None

    def init(self, db_url: str) -> None:
        if "postgresql" in db_url:
            connect_args = {"statement_cache_size": 0, "prepared_statement_cache_size": 0}
        else:
            connect_args = {}

        self._engine = asyncio.create_async_engine(url=db_url, pool_pre_ping=True, connect_args=connect_args)
        self._sessionmaker = asyncio.async_sessionmaker(bind=self._engine, expire_on_commit=False)

    async def close(self) -> None:
        if self._engine is None:
            return

        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[asyncio.AsyncSession]:
        if self._sessionmaker is None:
            raise IOError("Менажер сессии не прошел аутентификацию")
        async with self._sessionmaker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[asyncio.AsyncConnection]:
        if self._engine is None:
            raise IOError("Менажер сессии не прошел аутентификацию")
        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise


db_manager = DatabaseSessionManager()


async def get_async_db() -> asyncio.AsyncSession:
    async with db_manager.session() as session:
        yield session

