from datetime import datetime

from geojson_pydantic import Feature as BaseFeature, FeatureCollection as BaseFeatureCollection, Point
from pydantic import BaseModel


class Base(BaseModel):
    country: str
    city: str

    class Config:
        response_model = True


class Create(Base):
    ...


class Update(Base):
    ...


class Delete(Base):
    ...


# =============================


class GetFeatureProperties(Base):
    id: int
    created_date: datetime
    updated_date: datetime


class GetFeature(BaseFeature):
    geometry: Point
    properties: GetFeatureProperties


class GetFeatureCollection(BaseFeatureCollection):
    features: list[GetFeature]


# ==============================


class FeatureProperties(Base):
    ...


class Feature(BaseFeature):
    geometry: Point
    properties: FeatureProperties


class FeatureCollection(BaseFeatureCollection):
    features: list[Feature]

    class Config:
        response_model = True