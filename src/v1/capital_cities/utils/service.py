import shapely
from geoalchemy2 import WKBElement
from geoalchemy2.shape import from_shape

from src.core.database import Base


async def get_point_shape(data: Base) -> WKBElement:
    """- получить распарсенные данные в виде геоданных """
    geojson_feature = data.geom.features[0]
    coordinates = geojson_feature.geometry.coordinates
    return from_shape(shapely.Point(coordinates))

