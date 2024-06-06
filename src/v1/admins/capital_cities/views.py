from sqladmin import ModelView, Admin

from src.v1.capital_cities.models import CapitalCity


class CapitalCityAdmin(ModelView, model=CapitalCity):

    name = "Столицы городов"
    name_plural = "Столицы городов"
    # icon = "fa-solid fa-chart-line"

    # can_create = True
    # can_edit = False
    # can_delete = False
    # can_view_details = True

    category = "Города"

    column_list = [CapitalCity.id, CapitalCity.country, CapitalCity.city, 'longitude', 'latitude',
                   CapitalCity.created_date, CapitalCity.updated_date]

    column_details_list = [CapitalCity.country, CapitalCity.city, 'longitude', 'latitude',
                           CapitalCity.created_date, CapitalCity.updated_date,]

    # column_list = "__all__"
    # column_exclude_list = [CapitalCity.geom]

    # form_excluded_columns = [CapitalCity.geom]
    # column_formatters = {'Широта': lambda: 1,
    #                      'Долгота': lambda: 1}

    form_columns = [CapitalCity.country, CapitalCity.city,]

    column_labels = {CapitalCity.city: "Города", CapitalCity.country: "Страна",
                     CapitalCity.updated_date: "Дата обновления", CapitalCity.created_date: "Дата создания",
                     "longitude": "Долгота", "latitude": "Широта",}
    @classmethod
    def date_format(cls):
        return cls.strftime("%d.%m.%Y")

    column_type_formatters = dict(ModelView.column_type_formatters, created_date=date_format)

    save_as = True

async def register_views(app_admin: Admin) -> Admin:
    """- инициализация роутов """
    app_admin.add_view(CapitalCityAdmin)
    return app_admin
