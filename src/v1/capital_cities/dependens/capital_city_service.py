from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_async_db
from src.v1.capital_cities.reposituries.grud import CapitalCityGRUDRepository
from src.v1.capital_cities.services import CapitalCityService

async_db = Depends(get_async_db)


async def get_capital_city_service(db: AsyncSession = async_db) -> CapitalCityService:
    return CapitalCityService(CapitalCityGRUDRepository(db))


