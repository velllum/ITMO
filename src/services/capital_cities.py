from typing import Type, Sequence

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from ..core import database
from .. import schemas as schema, models as model
from ..models import CapitalCity


class CapitalCityService:
    """- сервисы (GRUD операции) столицы городов """

    def __init__(self, session: AsyncSession = Depends(database.get_async_db)):
        self.session = session

    async def get_list(self) -> Sequence[model.CapitalCity]:
        """- получить список пользователей """
        instance = await self.session.execute(select(model.CapitalCity))
        return instance.scalars().all()

    async def get_by_id(self, id: int) -> Type[CapitalCity]:
        """- получить по id """
        return await self.__check_an_id(id)

    async def create(self, data: schema.CreateCapital) -> model.CapitalCity:
        """- создать """

        # TODO: реализовать проверку на присутствие данных в базе, дабы не получить дубли

        obj = model.CapitalCity(**data.dict())
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, id: int, data: schema.UpdateCapital) -> Type[CapitalCity]:
        """- обновить """
        instance = await self.__check_an_id(id)
        instance.country = data.country
        instance.city = data.city
        instance.geom = data.geom
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def delete(self, id: int):
        """- удалить """
        instance = self.__check_an_id(id)
        await self.session.delete(instance)
        await self.session.commit()

    async def __check_an_id(self, id: int) -> Type[CapitalCity]:
        """- получить
        - если пользователь отсутствует отправляем ошибку 404"""
        instance = await self.session.get(model.CapitalCity, id)
        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ID НЕ НАЙДЕН')
        return instance
