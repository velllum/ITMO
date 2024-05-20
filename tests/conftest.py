from typing import AsyncGenerator, Any

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.testclient import TestClient

from src import routers as router, schemas as schema, create_app, settings
from src.core.database import db_manager


# @pytest.fixture
@pytest.fixture
def app() -> FastAPI:
    """- получить объект приложения """
    return create_app()


def pytest_configure(config):
    """- регистрация кастомных отметок """
    config.addinivalue_line("markers", "itmo_capital_cities: Группа тестов приложения основных городов стран")


@pytest.fixture
def client(app) -> TestClient:
    """- получить клиента """
    headers = {"Content-Type": "application/json"}
    base_url = f'http://{settings.WEB_HOST}:{settings.WEB_PORT}'
    with TestClient(app=app, base_url=base_url, headers=headers) as client:
        yield client


@pytest.fixture
def prefix() -> str:
    """- получить префикс ссылки """
    return f"{router.API_PREFIX}/capital-cities"


# @pytest.fixture
# async def sessionmanager():
#     """- инициализация менеджера сессии запроса к базе """
#     db_manager.init(settings.DATABASE_URL_ASYNCPG)
#     yield db_manager
#     await db_manager.close()
#
#
# @pytest.fixture
# async def db(sessionmanager) -> AsyncSession:
#     """- получить префикс ссылки """
#     async with db_manager.session() as session:
#         yield session
#
#
# @pytest.fixture
# async def dct_data() -> dict:
#     """- словарь с данными """
#     return {
#         "country": "Казахстан",
#         "city": "Астана",
#         "geom": {
#             "type": "FeatureCollection",
#             "features": [
#                 {
#                     "type": "Feature",
#                     "properties": {},
#                     "geometry": {
#                         "coordinates": [
#                             71.43075337936759,
#                             51.128427723406304
#                         ],
#                         "type": "Point"
#                     }
#                 }
#             ]
#         }
#     }
#
#
# @pytest.fixture
# async def schema_create(dct_data: dict) -> schema.Create:
#     return schema.Create(**dct_data)


@pytest.fixture
async def schema_update(dct_data: dict) -> schema.Update:
    return schema.Update(**dct_data)


