import logging
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from . import routers as router
from .core import settings
from .core.database import db_manager

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """- создаем приложение"""
    app = FastAPI(title="HTTP REST API", debug=settings.WEB_DEBUG)

    register_startup(app)
    register_shutdown(app)
    register_routers(app)
    register_cors(app)

    return app


def register_startup(app: FastAPI):
    """- запускается в начале работы"""
    @app.on_event("startup")
    async def handler():
        try:
            await start_database()
            logger.info("Запуск выполнен")
        except Exception as e:
            logger.exception(e, 'Сбой при запуске')


async def start_database():
    """- регистрируем подключение к базе данных"""
    logger.info("Запуск базы данных")
    db_manager.init(settings.DATABASE_URL_ASYNCPG)


def register_shutdown(app: FastAPI):
    """- запускается в конце"""
    @app.on_event("shutdown")
    async def handler():
        logger.info('Завершение работы')
        try:
            await close_database()
        except Exception as e:
            logger.exception(e, 'Сбой при выключении')


async def close_database():
    """- закрываем базу данных"""
    logger.info("Закрыть базу данных")
    await db_manager.close()


def register_routers(app: FastAPI):
    """- добавляем представлений"""
    logger.info("Запуск представлений")
    router.get_routers(app)


def register_cors(app):
    """- добавляем список разрешенных адрес для работы через фронт"""
    app.add_middleware(CORSMiddleware,
                       allow_origins=settings.WEB_ALLOW_ORIGINS,
                       allow_credentials=True,
                       allow_methods=["*"],
                       allow_headers=["*"],)

