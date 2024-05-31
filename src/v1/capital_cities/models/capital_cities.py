import shapely
import sqlalchemy as sa
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape, from_shape
from sqlalchemy.sql import func

from src.core.database import Base


class CapitalCity(Base):
    """- модель столицы городов """

    __tablename__ = "capital_cities"
    __table_args__ = (sa.UniqueConstraint('country', 'city', name='uq_capital_cities_country_city'),)

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    country = sa.Column(sa.String, index=True)
    city = sa.Column(sa.String, index=True)
    geom = sa.Column(Geometry('POINT'))

    created_date = sa.Column(sa.DateTime, server_default=func.now())
    updated_date = sa.Column(sa.DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f"CapitalCity(id={self.id!r}, country={self.country!r}, city={self.city!r}, geom={self.geom!r})"

    async def feature(self) -> dict:
        """- получить словарь в стиле GEOJSON """
        geom = to_shape(self.geom)
        return {
            "type": "Feature",
            "geometry": {
                "type": geom.geom_type,
                "coordinates": [geom.x, geom.y]
            },
            "properties": {
                "id": self.id,
                "country": self.country,
                "city": self.city,
                "created_date": self.created_date,
                "updated_date":  self.updated_date
            }
        }

    @staticmethod
    async def create(data):
        """- создать новый объект """
        features = data.features[0]
        instance = CapitalCity(
            country=features.properties.country,
            city=features.properties.city,
            geom=from_shape(shapely.Point(features.geometry.coordinates))
        )
        return instance

    @staticmethod
    async def update(instance, data):
        """- создать новый объект """
        features = data.features[0]
        instance.country = features.properties.country
        instance.city = features.properties.city
        instance.geom = from_shape(shapely.Point(features.geometry.coordinates))
        return instance

