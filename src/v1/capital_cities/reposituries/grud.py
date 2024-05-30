from abc import ABC, abstractmethod
from pprint import pprint

import shapely
from geoalchemy2 import WKBElement
from geoalchemy2.shape import from_shape
from sqlalchemy import select
from typing import Type, Sequence, Any

from asyncpg import UniqueViolationError
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.core.database import Base
from src.v1.capital_cities.models import CapitalCity
from src.v1.capital_cities.schemas.capital_cities import FeatureCollection


class AbstractRepository(ABC):

    @abstractmethod
    async def get_all(self, *args, **kwargs) -> None:
        """- получить список """
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, *args, **kwargs) -> None:
        """- получить экземпляр """
        raise NotImplementedError

    @abstractmethod
    async def create(self, *args, **kwargs) -> None:
        """- создать """
        raise NotImplementedError

    @abstractmethod
    async def update(self, *args, **kwargs) -> None:
        """- обновить """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, *args, **kwargs) -> None:
        """- удалить """
        raise NotImplementedError


class BaseGRUDRepository(AbstractRepository):

    model = None

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[Any]:
        """- получить список """
        instance = await self.db.execute(select(self.model).offset(skip).limit(limit))
        return instance.scalars().all()

    async def get_one(self, pk: int) -> Type[Any]:
        """- получить по pk """
        instance = await self.db.get(self.model, pk)
        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ID НЕ НАЙДЕН')
        return instance

    async def create(self, data: FeatureCollection):
        """- создать """
        pprint(data)

        try:
            obj = self.model(country=data.country, city=data.city, geom=await self.get_point_shape(data))
            self.db.add(obj)
            await self.db.commit()
            await self.db.refresh(obj)
            return obj
        except IntegrityError or UniqueViolationError:
            raise HTTPException(status_code=status.HTTP_200_OK, detail='СТРАНА И ГОРОД УЖЕ СУЩЕСТВУЮТ')

    async def update(self, pk: int, data: FeatureCollection) -> Type[Any]:
        """- обновить """
        instance = await self.get_one(pk)
        try:
            instance.country = data.country
            instance.city = data.city
            instance.geom = await self.get_point_shape(data)
            await self.db.commit()
            await self.db.refresh(instance)
            return instance
        except IntegrityError or UniqueViolationError:
            raise HTTPException(status_code=status.HTTP_200_OK, detail='СТРАНА И ГОРОД УЖЕ СУЩЕСТВУЮТ')

    async def delete(self, pk: int):
        """- удалить """
        instance = await self.get_one(pk)
        await self.db.delete(instance)
        await self.db.commit()

    @staticmethod
    async def get_point_shape(data) -> WKBElement:
        """- получить распарсенные данные в виде геоданных """
        geojson_feature = data.geom.features[0]
        coordinates = geojson_feature.geometry.coordinates
        return from_shape(shapely.Point(coordinates))


class CapitalCityGRUDRepository(BaseGRUDRepository):
    model = CapitalCity



