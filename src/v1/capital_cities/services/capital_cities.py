from typing import Any

from geoalchemy2.shape import to_shape
import geojson_pydantic

from src.v1.capital_cities.reposituries.grud import CapitalCityGRUDRepository
from src.v1.capital_cities.schemas import GetGeoJSONFeatureCollection, Create, Update, GetGeoJSONFeature


class CapitalCityService:
    """- сервисы (GRUD операции) столицы городов """

    def __init__(self, grud: CapitalCityGRUDRepository):
        self.grud = grud

    async def get_all(self, skip: int = 0, limit: int = 100) -> GetGeoJSONFeatureCollection:
        """- получить список пользователей """
        list_instance = await self.grud.get_all(skip, limit)
        features = [await self.get_geojson_feature(obj) for obj in list_instance]
        return GetGeoJSONFeatureCollection(type="FeatureCollection", features=features)

    async def get_one(self, pk: int) -> GetGeoJSONFeatureCollection:
        """- получить по pk """
        instance = await self.grud.get_one(pk)
        feature = await self.get_geojson_feature(instance)
        return GetGeoJSONFeatureCollection(type="FeatureCollection", features=[feature])

    async def create(self, data: Create) -> GetGeoJSONFeatureCollection:
        """- создать """
        instance = self.grud.create(data)
        feature = await self.get_geojson_feature(instance)
        return GetGeoJSONFeatureCollection(type="FeatureCollection", features=[feature])

    async def update(self, pk: int, data: Update) -> GetGeoJSONFeatureCollection:
        """- обновить """
        instance = await self.grud.update(pk, data)
        feature = await self.get_geojson_feature(instance)
        return GetGeoJSONFeatureCollection(type="FeatureCollection", features=[feature])

    async def delete(self, pk: int):
        """- удалить """
        await self.grud.delete(pk)

    @staticmethod
    async def get_geojson_feature(obj: Any) -> GetGeoJSONFeature:
        """- получить geojson """
        geom = to_shape(obj.geom)

        return GetGeoJSONFeature(
            # type="Feature",
            geometry=geojson_pydantic.Point(coordinates=[geom.x, geom.y], type=geom.geom_type),
            properties={"id": obj.id, "country": obj.country, "city": obj.city,
                        "created_date": obj.created_date, "updated_date": obj.updated_date}
        )

