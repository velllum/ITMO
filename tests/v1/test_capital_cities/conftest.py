import copy

import pytest
from fastapi import FastAPI
from sqlalchemy import select
from starlette.testclient import TestClient

from src.core.configs import settings
from src.v1 import API_PREFIX, create_app
from src.v1.capital_cities.models import CapitalCity
from src.v1.capital_cities.schemas import Create, Update
from tests.database import get_session


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
    return f"{API_PREFIX}/capital-cities"


@pytest.fixture
def db():
    """- получить синхронную сессию подключения к БД """
    session = get_session()
    yield session
    session.close()


@pytest.fixture
def dct_create_data() -> dict:
    """- словарь с данными создания """
    return {
        "country": "Казахстан",
        "city": "Астана",
        "geom": {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {},
                    "geometry": {
                        "coordinates": [
                            71.43075337936759,
                            51.128427723406304
                        ],
                        "type": "Point"
                    }
                }
            ]
        }
    }


@pytest.fixture
def dct_update_data(dct_create_data) -> dict:
    """- словарь с данными обновления """
    dct = copy.deepcopy(dct_create_data)
    dct['country'] = 'Литва'
    dct['city'] = 'Вильнюс'
    dct['geom']['features'][0]['geometry']['coordinates'] = [25.28303715486942, 54.686961697152384]
    return dct


@pytest.fixture
def schema_create(dct_create_data: dict) -> Create:
    return Create(**dct_create_data)


@pytest.fixture
def schema_update(dct_update_data: dict) -> Update:
    return Update(**dct_update_data)


@pytest.fixture
def instance_create(db, schema_create) -> CapitalCity:
    """- получить объект по полям страны и город, после сохранения """
    db_execute = db.execute(select(CapitalCity).where(
        CapitalCity.city == schema_create.city,
        CapitalCity.country == schema_create.country
    ))
    return db_execute.scalars().first()


@pytest.fixture
def instance_update(db, schema_update) -> CapitalCity:
    """- получить объект по полям страны и город, после обновления """
    db_execute = db.execute(select(CapitalCity).where(
        CapitalCity.city == schema_update.city,
        CapitalCity.country == schema_update.country
    ))
    return db_execute.scalars().first()


