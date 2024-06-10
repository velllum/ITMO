import shapely
from geoalchemy2.shape import from_shape
from sqladmin import ModelView, Admin

from src.v1.admins.capital_cities.forms import CreateCapitalCityAdminForm
from src.v1.capital_cities.models import CapitalCity


class CapitalCityAdmin(ModelView, model=CapitalCity):
    """- представление название городов """

    form = CreateCapitalCityAdminForm
    column_labels = {CapitalCity.city: "Города", CapitalCity.country: "Страна",
                     CapitalCity.updated_date: "Дата обновления", CapitalCity.created_date: "Дата создания",
                     "longitude": "Долгота", "latitude": "Широта", }
    name = "Столицы городов"
    name_plural = "Столицы городов"
    category = "Города"
    column_list = [CapitalCity.id, CapitalCity.country, CapitalCity.city, 'longitude', 'latitude',
                   CapitalCity.created_date, CapitalCity.updated_date]
    column_details_list = [CapitalCity.country, CapitalCity.city, 'longitude', 'latitude',
                           CapitalCity.created_date, CapitalCity.updated_date, ]

    async def on_model_change(self, data, model, is_created, request):
        """- переопределить метод при создании данных """
        if is_created is True:
            longitude = data.pop('longitude')
            latitude = data.pop('latitude')
            data['geom'] = from_shape(shapely.Point([longitude, latitude]))


async def register_views(app_admin: Admin) -> Admin:
    """- инициализация представления админ панели """
    app_admin.add_view(CapitalCityAdmin)
    return app_admin


