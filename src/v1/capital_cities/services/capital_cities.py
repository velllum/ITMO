from typing import Type, Any

from asyncpg import UniqueViolationError
from fastapi import Depends, HTTPException
from geoalchemy2 import WKBElement
from geoalchemy2.shape import from_shape, to_shape
import shapely
import geojson_pydantic
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.core.database import Base, get_async_db
from src.v1.capital_cities.models import CapitalCity
from src.v1.capital_cities.reposituries.grud import CapitalCitiesGRUDRepository
from src.v1.capital_cities.schemas import GetGeoJSONFeatureCollection, Create, Update, GetGeoJSONFeature


class CapitalCityService:
    """- сервисы (GRUD операции) столицы городов """

    # def __init__(self, db: AsyncSession = Depends(get_async_db)):
    #     self.db = db
    def __init__(self, grud: CapitalCitiesGRUDRepository = Depends()):
        self.grud = grud

    async def get_all(self, skip: int = 0, limit: int = 100) -> GetGeoJSONFeatureCollection:
        """- получить список пользователей """
        # instance = await self.db.execute(select(CapitalCity).offset(skip).limit(limit))
        list_instance = await self.grud.get_all(skip, limit)
        # features = [await self.get_geojson_feature(obj) for obj in list_instance.scalars().all()]
        features = [await self.get_geojson_feature(obj) for obj in list_instance]
        return GetGeoJSONFeatureCollection(type="FeatureCollection", features=features)

    async def get_one(self, pk: int) -> GetGeoJSONFeatureCollection:
        """- получить по pk """
        instance = await self.get_instance_to_id(self.db, pk)
        feature = await self.get_geojson_feature(instance)
        return GetGeoJSONFeatureCollection(type="FeatureCollection", features=[feature])

    async def create(self, data: Create) -> GetGeoJSONFeatureCollection:
        """- создать """
        obj = CapitalCity(country=data.country, city=data.city, geom=await self.get_point_shape(data))
        self.db.add(obj)
        obj = await self._valid_and_commit_data(obj)
        feature = await self.get_geojson_feature(obj)
        return GetGeoJSONFeatureCollection(type="FeatureCollection", features=[feature])

    async def update(self, pk: int, data: Update) -> GetGeoJSONFeatureCollection:
        """- обновить """
        instance = await self.get_instance_to_id(self.db, pk)
        instance.country = data.country
        instance.city = data.city
        instance.geom = await self.get_point_shape(data)

        instance = await self._valid_and_commit_data(instance)
        feature = await self.get_geojson_feature(instance)
        return GetGeoJSONFeatureCollection(type="FeatureCollection", features=[feature])

    async def delete(self, pk: int):
        """- удалить """
        instance = await self.get_instance_to_id(self.db, pk)
        await self.db.delete(instance)
        await self.db.commit()

    async def _valid_and_commit_data(self, obj: Any) -> CapitalCity:
        """- добавление данных, проверить данные на существование в базе """
        try:
            await self.db.commit()
            await self.db.refresh(obj)
            return obj
        except IntegrityError or UniqueViolationError:
            raise HTTPException(status_code=status.HTTP_200_OK, detail='СТРАНА И ГОРОД УЖЕ СУЩЕСТВУЮТ')

    @staticmethod
    async def get_point_shape(data: Base) -> WKBElement:
        """- получить распарсенные данные в виде геоданных """
        geojson_feature = data.geom.features[0]
        coordinates = geojson_feature.geometry.coordinates
        return from_shape(shapely.Point(coordinates))

    @staticmethod
    async def get_geojson_feature(obj: Any) -> GetGeoJSONFeature:
        """- получить geojson """
        geom = to_shape(obj.geom)

        return GetGeoJSONFeature(
            type="Feature",
            geometry=geojson_pydantic.Point(coordinates=[geom.x, geom.y], type=geom.geom_type),
            properties={"id": obj.id, "country": obj.country, "city": obj.city,
                        "created_date": obj.created_date, "updated_date": obj.updated_date}
        )

    @staticmethod
    async def get_instance_to_id(db: AsyncSession, pk: int) -> Type[CapitalCity]:
        """- получить объект по ID
        - если пользователь отсутствует отправляем ошибку 404 """
        instance = await db.get(CapitalCity, pk)
        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ID НЕ НАЙДЕН')
        return instance

