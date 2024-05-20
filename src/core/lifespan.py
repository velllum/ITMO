import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import delete

from src import routers
from src.core import settings
from src.core.database import db_manager
from src.models import CapitalCity

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """- События продолжительности жизни """
    await start_database()
    # await clear_test_data_table()
    try:
        await add_test_data_table()
    except:
        pass
    await register_routers(app)

    yield

    await close_database()


async def start_database():
    """- регистрируем подключение к базе данных"""
    db_manager.init(settings.DATABASE_URL_ASYNCPG)
    logger.info("ЗАПУСК БАЗЫ ДАННЫХ ВЫПОЛНЕН")


async def clear_test_data_table():
    """- очистить тестовых данных """
    async with db_manager.session() as session:
        async with session.begin():
            await session.execute(delete(CapitalCity))
            await session.commit()
    logger.info("ОЧИСТКА ТАБЛИЦЫ ВЫПОЛНЕНА ВЫПОЛНЕН")


async def add_test_data_table():
    """- добавление тестовых данных """
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


async def register_routers(app: FastAPI):
    """- добавляем представлений"""
    routers.get_routers(app)
    logger.info("ЗАПУСК ПРЕДСТАВЛЕНИЙ")


async def close_database():
    """- закрываем базу данных"""
    await db_manager.close()
    logger.info("БАЗА ДАННЫХ ЗАКРЫТА")


