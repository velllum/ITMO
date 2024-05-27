from typing import Any, Type

import geojson_pydantic
import shapely
from fastapi import HTTPException
from geoalchemy2 import WKBElement
from geoalchemy2.shape import to_shape, from_shape
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.core.database import Base
from src.v1.capital_cities.models import CapitalCity
from src.v1.capital_cities.schemas import GetGeoJSONFeature


async def get_point_shape(data: Base) -> WKBElement:
    """- получить распарсенные данные в виде геоданных """
    geojson_feature = data.geom.features[0]
    coordinates = geojson_feature.geometry.coordinates
    return from_shape(shapely.Point(coordinates))


async def get_geojson_feature(obj: Any) -> GetGeoJSONFeature:
    """- получить geojson """
    geom = to_shape(obj.geom)

    return GetGeoJSONFeature(
        type="Feature",
        geometry=geojson_pydantic.Point(coordinates=[geom.x, geom.y], type=geom.geom_type),
        properties={"id": obj.id, "country": obj.country, "city": obj.city,
                    "created_date": obj.created_date, "updated_date": obj.updated_date})


async def get_instance_to_id(db: AsyncSession, pk: int) -> Type[CapitalCity]:
    """- получить объект по ID
    - если пользователь отсутствует отправляем ошибку 404 """
    instance = await db.get(CapitalCity, pk)
    if not instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ID НЕ НАЙДЕН')
    return instance

