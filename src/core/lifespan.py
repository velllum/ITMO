import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.configs import settings
from src.core.database import db_manager
from src.core.routers import register_routers
from src.v1.capital_cities.models import CapitalCity

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """- События продолжительности жизни """
    await start_database()
    await add_test_data_table()
    await start_routers(app)

    yield

    await close_database()


async def start_database():
    """- регистрируем подключение к базе данных"""
    db_manager.init(settings.DATABASE_URL_ASYNCPG)
    logger.info("ЗАПУСК БАЗЫ ДАННЫХ ВЫПОЛНЕН")


async def start_routers(app: FastAPI):
    """- старт инициализации роутеров """
    await register_routers(app)
    logger.info("РЕГИСТРАЦИЯ РОУТОВ")


async def add_test_data_table():
    """- добавление тестовых данных """
    try:
        async with db_manager.session() as session:
            async with session.begin():
                capitals = [
                    CapitalCity(country="Россия", city="Москва", geom='POINT(37.6156 55.7520)'),
                    CapitalCity(country="Украина", city="Киев", geom='POINT(30.5234 50.4501)'),
                    CapitalCity(country="Беларусь", city="Минск", geom='POINT(27.5670 53.9000)'),
                ]
                session.add_all(capitals)
                await session.commit()
        logger.info("ДОБАВЛЕНИЕ ТЕСТОВЫХ ДАННЫХ ВЫПОЛНЕНО")
    except:
        pass


async def close_database():
    """- закрываем базу данных"""
    await db_manager.close()
    logger.info("БАЗА ДАННЫХ ЗАКРЫТА")

