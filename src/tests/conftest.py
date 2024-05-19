import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from .. import create_app, routers as router


@pytest.fixture
def app() -> FastAPI:
    """- получить объект приложения"""
    yield create_app()


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    """- получить клиента"""
    with TestClient(app) as client:
        yield client


@pytest.fixture
def prefix() -> str:
    """- получить префикс ссылки"""
    yield router.API_PREFIX


@pytest.fixture
def data() -> dict:
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
