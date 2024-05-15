from datetime import datetime
from typing import Optional

from geojson_pydantic import Feature, FeatureCollection
from pydantic import BaseModel


class BaseCapital(BaseModel):
    country: str
    city: str
    geom: dict


class GetCapital(BaseCapital):
    id: int
    created_date: datetime
    updated_date: datetime

    class Config:
        from_attributes = True


class CreateCapital(BaseCapital):
    ...


class UpdateCapital(BaseCapital):
    ...


class DeleteCapital(BaseCapital):
    ...


class CapitalGeoJSON(Feature):
    properties: Optional[GetCapital] = None


class CapitalsGeoJSON(FeatureCollection):
    features: list[CapitalGeoJSON]


