import logging

from fastapi import FastAPI
from sqladmin import Admin

from src.core.configs import settings
from src.core.database import db_manager
from src.v1.admins.capital_cities.views import register_views

logger = logging.getLogger(__name__)


async def create_admin(app: FastAPI) -> Admin:
    """- создаем админ панель """
    app_admin = Admin(app=app, title='Админ панель', engine=db_manager._engine, debug=settings.WEB_DEBUG)
    await register_views(app_admin)
    return app_admin


