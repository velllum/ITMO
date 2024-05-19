from geojson_pydantic import Feature, FeatureCollection, Point
from pydantic import BaseModel


class Base(BaseModel):
    country: str
    city: str
    geom: FeatureCollection


class Create(Base):
    ...


class Update(Base):
    ...


class Delete(Base):
    ...


class GetGeoJSONFeature(Feature):
    geometry: Point
    properties: dict


class GetGeoJSONFeatureCollection(FeatureCollection):
    features: list[GetGeoJSONFeature]



