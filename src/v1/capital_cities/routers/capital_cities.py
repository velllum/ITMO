from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import Response

from src.v1.capital_cities.dependens.capital_city_service import get_capital_city_service
from src.v1.capital_cities.schemas import GeoJSONFeatureCollection, Update, Create
from src.v1.capital_cities.services import CapitalCityService

router = APIRouter(prefix='/capital-cities', tags=['capital_cities'])
capital_city_service = Annotated[CapitalCityService, Depends(get_capital_city_service)]


@router.get('/', response_model=GeoJSONFeatureCollection)
async def get_all(service: capital_city_service, skip: int = 0, limit: int = 100) -> GeoJSONFeatureCollection:
    """- получить список """
    return await service.get_all(skip=skip, limit=limit)


@router.get('/{pk}', response_model=GeoJSONFeatureCollection)
async def get_by_pk(service: capital_city_service, pk: int) -> GeoJSONFeatureCollection:
    """- получить по pk """
    return await service.get_one(pk)


@router.post('/create', response_model=GeoJSONFeatureCollection)
async def create(service: capital_city_service, data: Create) -> GeoJSONFeatureCollection:
    """- создать """
    return await service.create(data)


@router.put('/{pk}', response_model=GeoJSONFeatureCollection)
async def update(service: capital_city_service, pk: int, data: Update) -> GeoJSONFeatureCollection:
    """- обновить """
    return await service.update(pk, data)


@router.delete('/{pk}', status_code=status.HTTP_200_OK)
async def delete(service: capital_city_service, pk: int) -> Response:
    """- удалить """
    await service.delete(pk)
    return Response(status_code=status.HTTP_200_OK, content='{"detail": "ДАННЫЕ УДАЛЕНЫ"}')


