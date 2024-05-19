import logging

from fastapi import FastAPI
from sqlalchemy import delete
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from . import routers as router
from .core import settings
from .core.database import db_manager, get_async_db
from .models import CapitalCity

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """- создаем приложение"""
    app = FastAPI(title="HTTP REST API", debug=settings.WEB_DEBUG)
    register_startup(app)
    register_shutdown(app)
    register_routers(app)
    register_middleware(app)
    return app


def register_startup(app: FastAPI):
    """- запускается в начале работы"""
    @app.on_event("startup")
    async def handler():
        await start_database()
        await clear_test_data_table()
        await add_test_data_table()


async def clear_test_data_table():
    """- очистить тестовых данных """
    async with db_manager.session() as session:
        async with session.begin():
            await session.execute(delete(CapitalCity))
            await session.commit()
    logger.info("ОЧИСТКА ТАБЛИЦЫ ВЫПОЛНЕНА ВЫПОЛНЕН")


async def start_database():
    """- регистрируем подключение к базе данных"""
    db_manager.init(settings.DATABASE_URL_ASYNCPG)
    logger.info("ЗАПУСК БАЗЫ ДАННЫХ ВЫПОЛНЕН")


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


def register_shutdown(app: FastAPI):
    """- запускается в конце"""
    @app.on_event("shutdown")
    async def handler():
        try:
            await close_database()
            logger.info('ЗАВЕРШЕНИЕ РАБОТЫ')
        except Exception as e:
            logger.exception(e, 'СБОЙ ПРИ ВЫКЛЮЧЕНИИ')


async def close_database():
    """- закрываем базу данных"""
    await db_manager.close()
    logger.info("ЗАКРЫТЬ БАЗУ ДАННЫХ")


def register_routers(app: FastAPI):
    """- добавляем представлений"""
    router.get_routers(app)
    logger.info("ЗАПУСК ПРЕДСТАВЛЕНИЙ")


def register_middleware(app):
    """- регистрация промежуточного программного ПО """
    app.add_middleware(CORSMiddleware,
                       allow_origins=settings.WEB_ALLOW_ORIGINS,
                       allow_credentials=True,
                       allow_methods=["*"],
                       allow_headers=["*"],)

    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.WEB_ALLOW_HOSTS.split())


