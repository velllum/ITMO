from src.v1.capital_cities.reposituries.grud import CapitalCitiesGRUDRepository
from src.v1.capital_cities.services import CapitalCityService


def get_capital_city_service():
    return CapitalCityService(CapitalCitiesGRUDRepository)
