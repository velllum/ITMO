from typing import Any

from geoalchemy2.shape import to_shape
from geojson_pydantic import Point

from src.v1.capital_cities.reposituries.grud import CapitalCityGRUDRepository
from src.v1.capital_cities.schemas import GeoJSONFeatureCollection, Create, Update, GeoJSONFeature
from src.v1.capital_cities.schemas.capital_cities import FeatureProperties


class CapitalCityService:
    """- сервисы (GRUD операции) столицы городов """

    def __init__(self, grud: CapitalCityGRUDRepository):
        self.grud = grud

    async def get_all(self, skip: int = 0, limit: int = 100) -> GeoJSONFeatureCollection:
        """- получить список пользователей """
        list_instance = await self.grud.get_all(skip, limit)
        features = [await self.get_geojson_feature(obj) for obj in list_instance]
        return GeoJSONFeatureCollection(type="FeatureCollection", features=features)

    async def get_one(self, pk: int) -> GeoJSONFeatureCollection:
        """- получить по pk """
        instance = await self.grud.get_one(pk)
        feature = await self.get_geojson_feature(instance)
        return GeoJSONFeatureCollection(type="FeatureCollection", features=[feature])

    async def create(self, data: Create) -> GeoJSONFeatureCollection:
        """- создать """
        instance = self.grud.create(data)
        feature = await self.get_geojson_feature(instance)
        return GeoJSONFeatureCollection(type="FeatureCollection", features=[feature])

    async def update(self, pk: int, data: Update) -> GeoJSONFeatureCollection:
        """- обновить """
        instance = await self.grud.update(pk, data)
        feature = await self.get_geojson_feature(instance)
        return GeoJSONFeatureCollection(type="FeatureCollection", features=[feature])

    async def delete(self, pk: int):
        """- удалить """
        await self.grud.delete(pk)

    @staticmethod
    async def get_geojson_feature(instance: Any) -> GeoJSONFeature:
        """- получить geojson """
        geom = to_shape(instance.geom)

        return GeoJSONFeature(
            type="Feature",
            geometry=Point(coordinates=[geom.x, geom.y], type=geom.geom_type),
            properties=FeatureProperties(**instance.__dict__)
        )

