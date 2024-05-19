from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import Response

from .. import schemas as schema, services as service

router = APIRouter(prefix='/capital-cities', tags=['capital_cities'])


@router.get('/', response_model=schema.GetGeoJSONFeatureCollection)
async def get_all(skip: int = 0, limit: int = 100, serv: service.CapitalCityService = Depends()) -> schema.GetGeoJSONFeatureCollection:
    """- получить список """
    return await serv.get_all(skip=skip, limit=limit)


@router.get('/{pk}', response_model=schema.GetGeoJSONFeatureCollection)
async def get_by_pk(pk: int, serv: service.CapitalCityService = Depends()) -> schema.GetGeoJSONFeatureCollection:
    """- получить по pk """
    return await serv.get_one(pk)


@router.post('/create', response_model=schema.GetGeoJSONFeatureCollection)
async def create(data: schema.Create, serv: service.CapitalCityService = Depends()) -> schema.GetGeoJSONFeatureCollection:
    """- создать """
    return await serv.create(data)


@router.put('/{pk}', response_model=schema.GetGeoJSONFeatureCollection)
async def update(pk: int, data: schema.Update, serv: service.CapitalCityService = Depends()) -> schema.GetGeoJSONFeatureCollection:
    """- обновить """
    return await serv.update(pk, data)


@router.delete('/{pk}', status_code=status.HTTP_200_OK)
async def delete(pk: int, serv: service.CapitalCityService = Depends()) -> Response:
    """- удалить """
    await serv.delete(pk)
    return Response(status_code=status.HTTP_200_OK, content='{"detail": "ДАННЫЕ УДАЛЕНЫ"}')
