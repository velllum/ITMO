from typing import Any

from src.v1.capital_cities.reposituries.grud import CapitalCityGRUDRepository
from src.v1.capital_cities.schemas.capital_cities import FeatureCollection


class CapitalCityService:
    """- сервисы (GRUD операции) столицы городов """

    def __init__(self, grud: CapitalCityGRUDRepository):
        self.features = []
        self.grud = grud

    async def get_all(self, skip: int = 0, limit: int = 100) -> dict[str, str | list[Any]]:
        """- получить список пользователей """
        list_instance = await self.grud.get_all(skip, limit)
        self.features = [await instance.feature() for instance in list_instance]
        return await self.__feature_collection()

    async def get_one(self, pk: int):
        """- получить по pk """
        self.features = await self.grud.get_one(pk)
        return await self.__feature_collection()

    async def create(self, data: FeatureCollection) -> dict[str, str | list[Any]]:
        """- создать """
        print(data)
        self.features = self.grud.create(data)
        return await self.__feature_collection()

    async def update(self, pk: int, data: FeatureCollection) -> dict[str, str | list[Any]]:
        """- обновить """
        self.features = await self.grud.update(pk, data)
        return await self.__feature_collection()

    async def delete(self, pk: int):
        """- удалить """
        await self.grud.delete(pk)

    async def __feature_collection(self) -> dict[str, str | list[Any]]:
        """- получить коллекцию в стиле GEOJSON """
        return {"type": "FeatureCollection", "features": self.features}


