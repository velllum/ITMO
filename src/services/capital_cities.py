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

from ..core import database
from .. import schemas as schema, models as model
from ..schemas import GetGeoJSONFeatureCollection


class CapitalCityService:
    """- сервисы (GRUD операции) столицы городов """

    def __init__(self, db: AsyncSession = Depends(database.get_async_db)):
        self.db = db

    async def get_all(self, skip: int = 0, limit: int = 100) -> schema.GetGeoJSONFeatureCollection:
        """- получить список пользователей """
        instance = await self.db.execute(select(model.CapitalCity).offset(skip).limit(limit))
        features = [await self._get_geojson_feature(obj) for obj in instance.scalars().all()]
        return schema.GetGeoJSONFeatureCollection(type="FeatureCollection", features=features)

    async def get_one(self, pk: int) -> schema.GetGeoJSONFeatureCollection:
        """- получить по pk """
        instance = await self._get_obj_to_id(pk)
        feature = await self._get_geojson_feature(instance)
        return schema.GetGeoJSONFeatureCollection(type="FeatureCollection", features=[feature])

    async def create(self, data: schema.Create) -> schema.GetGeoJSONFeatureCollection:
        """- создать """
        obj = model.CapitalCity(country=data.country, city=data.city, geom=await self._get_shape(data))
        self.db.add(obj)
        obj = await self._valid_and_commit_data(obj)
        feature = await self._get_geojson_feature(obj)
        return schema.GetGeoJSONFeatureCollection(type="FeatureCollection", features=[feature])

    async def update(self, pk: int, data: schema.Update) -> GetGeoJSONFeatureCollection:
        """- обновить """
        instance = await self._get_obj_to_id(pk)
        instance.country = data.country
        instance.city = data.city
        instance.geom = await self._get_shape(data)
        await self.db.commit()
        await self.db.refresh(instance)

        feature = await self._get_geojson_feature(instance)
        return schema.GetGeoJSONFeatureCollection(type="FeatureCollection", features=[feature])

    async def delete(self, pk: int):
        """- удалить """
        instance = await self._get_obj_to_id(pk)
        await self.db.delete(instance)
        await self.db.commit()

    async def _valid_and_commit_data(self, obj: Any) -> model.CapitalCity:
        """- добавление данных, проверить данные на существование в базе """
        try:
            await self.db.commit()
            await self.db.refresh(obj)
            return obj
        except IntegrityError or UniqueViolationError:
            raise HTTPException(status_code=status.HTTP_200_OK, detail='СТРАНА И ГОРОД УЖЕ СУЩЕСТВУЮТ')

    @staticmethod
    async def _get_shape(data: schema.Base) -> WKBElement:
        """- получить распарсенные данные в виде геоданных """
        geojson_feature = data.geom.features[0]
        coordinates = geojson_feature.geometry.coordinates
        return from_shape(shapely.Point(coordinates))

    @staticmethod
    async def _get_geojson_feature(obj: Any) -> schema.GetGeoJSONFeature:
        """- получить geojson """
        geom = to_shape(obj.geom)

        return schema.GetGeoJSONFeature(
            type="Feature",
            geometry=geojson_pydantic.Point(coordinates=[geom.x, geom.y], type=geom.geom_type),
            properties={"id": obj.id, "country": obj.country, "city": obj.city,
                        "created_date": obj.created_date, "updated_date": obj.updated_date}
        )

    async def _get_obj_to_id(self, pk: int) -> Type[model.CapitalCity]:
        """- получить объект по ID
        - если пользователь отсутствует отправляем ошибку 404 """
        instance = await self.db.get(model.CapitalCity, pk)
        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ID НЕ НАЙДЕН')
        return instance

