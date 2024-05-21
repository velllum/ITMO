import logging
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session

from src.core import settings

logger = logging.getLogger(__name__)


def get_engine() -> Engine:
    # получить объект подключения к базе
    return create_engine(url=settings.DATABASE_URL_PSYCOPG)


def get_session() -> Session:
    """- создаем сессию"""
    return sessionmaker(bind=get_engine())()

