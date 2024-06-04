import logging

from fastapi import FastAPI
from sqladmin import Admin

from src.core.configs import settings
from src.core.database import db_manager

logger = logging.getLogger(__name__)


async def create_admin(app: FastAPI) -> Admin:
    """- создаем админ панель """
    admin = Admin(app=app, engine=db_manager.connect(), debug=settings.WEB_DEBUG)
    return admin


# async def start_admin(app: FastAPI):
#     """- регистрируем админ-панель """
#     app_admin = await create_admin(app)
#     logger.info("ЗАПУСК АДМИН ПАНЕЛИ")
#
#
# async def add_view_admin(app: Admin):
#     """- регистрируем представления админ-панель """
#     app_admin = await create_admin(app)
#     logger.info("РЕГИСТРАЦИЯ ПЕРЕДСТАВЛЕНИЙ АДМИН ПАНЕЛИ")

