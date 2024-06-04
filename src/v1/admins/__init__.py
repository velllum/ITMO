import logging

from fastapi import FastAPI
from sqladmin import Admin

logger = logging.getLogger(__name__)


def create_admin(app: FastAPI) -> Admin:
    """- создаем админ панель """
    admin = Admin(app, engine)
    return admin
