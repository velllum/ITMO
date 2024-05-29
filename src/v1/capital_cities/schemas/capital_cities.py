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


class FeatureProperties(BaseModel):
    id: int
    country: str
    city: str
    created_date: datetime
    updated_date: datetime

    class config:
        response_model = True


class GeoJSONFeature(Feature):
    geometry: Point
    properties: FeatureProperties


class GeoJSONFeatureCollection(FeatureCollection):
    features: list[GeoJSONFeature]


