import copy

import pytest
from fastapi import FastAPI
from geojson_pydantic.types import Position2D, Position3D
from sqlalchemy import select
from starlette.testclient import TestClient

from src.core.configs import settings
from src.core.database import get_session
from src.v1 import API_PREFIX, create_app
from src.v1.capital_cities.models import CapitalCity
from src.v1.capital_cities.schemas.capital_cities import FeatureCollection, FeatureProperties


@pytest.fixture
def app() -> FastAPI:
    """- получить объект приложения """
    return create_app()


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
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        71.43075337936759,
                        51.128427723406304
                    ],
                },
                "properties": {
                    "country": "Казахстан",
                    "city": "Астана"
                }
            }
        ]
    }


@pytest.fixture
def dct_update_data(dct_create_data) -> dict:
    """- словарь с данными обновления """
    dct_copy = copy.deepcopy(dct_create_data)
    dct = dct_copy['features'][0]
    dct['properties']['country'] = 'Литва'
    dct['properties']['city'] = 'Вильнюс'
    dct['geometry']['coordinates'] = [25.28303715486942, 54.686961697152384]
    return dct_copy


@pytest.fixture
def schema_create(dct_create_data: dict) -> FeatureCollection:
    return FeatureCollection(**dct_create_data)


@pytest.fixture
def schema_update(dct_update_data: dict) -> FeatureCollection:
    return FeatureCollection(**dct_update_data)


@pytest.fixture
def coordinates_create(schema_create) -> Position2D | Position3D:
    return schema_create.features[0].geometry.coordinates


@pytest.fixture
def properties_create(schema_create) -> FeatureProperties:
    return schema_create.features[0].properties


@pytest.fixture
def coordinates_update(schema_update) -> Position2D | Position3D:
    return schema_update.features[0].geometry.coordinates


@pytest.fixture
def properties_update(schema_update) -> FeatureProperties:
    return schema_update.features[0].properties


@pytest.fixture
def instance_create(db, properties_create) -> CapitalCity:
    """- получить объект по полям страны и город, после сохранения """
    db_execute = db.execute(select(CapitalCity).where(
        CapitalCity.city == properties_create.city,
        CapitalCity.country == properties_create.country
    ))
    return db_execute.scalars().first()


@pytest.fixture
def instance_update(db, properties_update) -> CapitalCity:
    """- получить объект по полям страны и город, после обновления """
    db_execute = db.execute(select(CapitalCity).where(
        CapitalCity.city == properties_update.city,
        CapitalCity.country == properties_update.country
    ))
    return db_execute.scalars().first()


def pytest_configure(config):
    """- регистрация кастомных отметок """
    config.addinivalue_line("markers", "itmo_capital_cities: Группа тестов приложения основных городов стран")



