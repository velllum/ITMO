from fastapi import FastAPI

from src import v1
from src.v1.capital_cities.routers.capital_cities import router as router_capital_cities


async def register_routers(app: FastAPI) -> FastAPI:
    """- инициализация роутов """
    app.include_router(router=router_capital_cities, prefix=v1.API_PREFIX)
    return app