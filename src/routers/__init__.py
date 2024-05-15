from fastapi import FastAPI

from . import capital_cities


VERSION_PREFIX = 'v1'
API_PREFIX = f'/api/{VERSION_PREFIX}'


def get_routers(app: FastAPI) -> FastAPI:
    """- инициализация роутов"""
    # подключаем роут пользователя
    app.include_router(capital_cities.router, prefix=API_PREFIX)
    return app
