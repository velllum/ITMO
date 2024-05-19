import sqlalchemy as sa
from geoalchemy2 import Geometry
from sqlalchemy.sql import func

from ..core import database


class CapitalCity(database.Base):
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

