from typing import List, Type, Sequence

from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import Response

from .. import schemas as schema, services as service
from ..models import CapitalCity

router = APIRouter(prefix='/capital-cities', tags=['capital_cities'])


@router.get('/', response_model=List[schema.GetCapital])
async def get_list(session: service.CapitalCityService = Depends()) -> Sequence[schema.GetCapital]:
    """- получить список """
    return await session.get_list()


@router.get('/{id}', response_model=schema.GetCapital)
async def get_by_id(id: int, session: service.CapitalCityService = Depends()) -> Type[CapitalCity]:
    """- получить по id """
    return await session.get_by_id(id)


@router.post('/create', response_model=schema.GetCapital)
async def create(data: schema.CreateCapital, session: service.CapitalCityService = Depends()) -> CapitalCity:
    """- создать """
    return await session.create(data)


@router.put('/{id}', response_model=schema.GetCapital)
async def update(id: int, data: schema.UpdateCapital,
                 session: service.CapitalCityService = Depends()) -> Type[CapitalCity]:
    """- обновить """
    return await session.update(id, data)


@router.delete('/{id}', status_code=status.HTTP_200_OK)
async def delete(id: int, session: service.CapitalCityService = Depends()) -> Response:
    """- удалить """
    await session.delete(id)
    return Response(status_code=status.HTTP_200_OK, content="ДАННЫЕ УДАЛЕНЫ")
