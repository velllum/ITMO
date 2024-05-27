from abc import ABC, abstractmethod
from typing import Type, Any

from fastapi import Depends

from src.v1.capital_cities.models import CapitalCity
from src.v1.capital_cities.reposituries.grud import CapitalCitiesGRUDRepository
from src.v1.capital_cities.schemas import Create, Update, GetGeoJSONFeatureCollection
from src.v1.capital_cities.utils import get_point_shape, get_geojson_feature


class AbstractGeoJSONRepository(ABC):

    @abstractmethod
    async def get_all(self, *args, **kwargs) -> None:
        """- получить список """
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, *args, **kwargs) -> None:
        """- получить экземпляр """
        raise NotImplementedError


class BaseGeoJSONRepository(AbstractGeoJSONRepository):

    def __init__(self, grud: CapitalCitiesGRUDRepository = Depends()):
        self.grud = grud

    async def get_all(self, instance: Any) -> GetGeoJSONFeatureCollection:
        """- получить список """
        list_instance = await self.grud.get_all(skip, limit)
        features = [await get_geojson_feature(obj) for obj in instance]
        return GetGeoJSONFeatureCollection(type="FeatureCollection", features=features)

    async def get_one(self, instance: Any) -> Type[Any]:
        """- получить экземпляр """



class CapitalCitiesGeoJSONRepository(BaseGeoJSONRepository):
    schema = GetGeoJSONFeatureCollection


