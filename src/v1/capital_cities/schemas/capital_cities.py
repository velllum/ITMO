from datetime import datetime

from geojson_pydantic import Feature, FeatureCollection, Point
from pydantic import BaseModel


class Base(BaseModel):
    country: str
    city: str


class Create(Base):
    geom: FeatureCollection


class Update(Base):
    geom: FeatureCollection


class Delete(Base):
    ...


class GetFeatureProperties(Base):
    id: int
    created_date: datetime
    updated_date: datetime

    class config:
        response_model = True


class GetGeoJSONFeature(Feature):
    geometry: Point
    properties: GetFeatureProperties




class GetGeoJSONFeatureCollection(FeatureCollection):
    features: list[GetGeoJSONFeature]


