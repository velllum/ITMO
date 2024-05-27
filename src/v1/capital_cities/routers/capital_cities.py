from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import Response

from src.v1.capital_cities.schemas import GetGeoJSONFeatureCollection, Update, Create
from src.v1.capital_cities.services import CapitalCityService

router = APIRouter(prefix='/capital-cities', tags=['capital_cities'])


@router.get('/', response_model=GetGeoJSONFeatureCollection)
async def get_all(skip: int = 0, limit: int = 100, serv: CapitalCityService = Depends()) -> GetGeoJSONFeatureCollection:
    """- получить список """
    return await serv.get_all(skip=skip, limit=limit)


@router.get('/{pk}', response_model=GetGeoJSONFeatureCollection)
async def get_by_pk(pk: int, serv: CapitalCityService = Depends()) -> GetGeoJSONFeatureCollection:
    """- получить по pk """
    return await serv.get_one(pk)


@router.post('/create', response_model=GetGeoJSONFeatureCollection)
async def create(data: Create, serv: CapitalCityService = Depends()) -> GetGeoJSONFeatureCollection:
    """- создать """
    return await serv.create(data)


@router.put('/{pk}', response_model=GetGeoJSONFeatureCollection)
async def update(pk: int, data: Update, serv: CapitalCityService = Depends()) -> GetGeoJSONFeatureCollection:
    """- обновить """
    return await serv.update(pk, data)


@router.delete('/{pk}', status_code=status.HTTP_200_OK)
async def delete(pk: int, serv: CapitalCityService = Depends()) -> Response:
    """- удалить """
    await serv.delete(pk)
    return Response(status_code=status.HTTP_200_OK, content='{"detail": "ДАННЫЕ УДАЛЕНЫ"}')
