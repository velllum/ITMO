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


class GetGeoJSONFeature(Feature):
    geometry: Point
    properties: dict


class GetGeoJSONFeatureCollection(FeatureCollection):
    features: list[GetGeoJSONFeature]


