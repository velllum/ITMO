import shapely
import wtforms
from geoalchemy2.shape import from_shape
from sqladmin import ModelView, Admin
from wtforms.validators import DataRequired

from src.v1.capital_cities.models import CapitalCity


class CreateCapitalCityAdminForm(wtforms.Form):
    """- форма создания столицы городов """
    country  = wtforms.StringField("Страна", validators=[DataRequired()], render_kw={"class": "form-control"})
    city  = wtforms.StringField("Города", render_kw={"class": "form-control"})
    longitude  = wtforms.DecimalField("Долгота", render_kw={"class": "form-control"})
    latitude  = wtforms.DecimalField("Широта", render_kw={"class": "form-control"})

    class Meta:
        locales = ['ru_RU', 'ru']


class CapitalCityAdmin(ModelView, model=CapitalCity):

    form = CreateCapitalCityAdminForm

    column_labels = {CapitalCity.city: "Города", CapitalCity.country: "Страна",
                     CapitalCity.updated_date: "Дата обновления", CapitalCity.created_date: "Дата создания",
                     "longitude": "Долгота", "latitude": "Широта",}

    async def on_model_change(self, data, model, is_created, request):

        print('111111', data)

        if is_created is True:
            longitude = data.pop('longitude')
            latitude = data.pop('latitude')
            data['geom'] = from_shape(shapely.Point([longitude, latitude]))


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



    # @classmethod
    # def date_format(cls):
    #     return cls.strftime("%d.%m.%Y")
    #
    # column_type_formatters = dict(ModelView.column_type_formatters, created_date=date_format)
    # form_converter =
    # save_as = True

    # form_overrides = dict(country=simple.TextAreaField)
    # form_args = dict(city=dict(label="sdfsdfsdfsdfsd"))
    # form_widget_args = dict(city=dict(readonly=True))
    #
    # form_ajax_refs = {
    #     'longitude': {
    #         'fields': ('geom', 'zip_code'),
    #     }
    # }
    #
    # def edit_form_query(self, request):
    #     edite_form = super().edit_form_query(request)
    #     print(type(edite_form))
    #     return edite_form


async def register_views(app_admin: Admin) -> Admin:
    """- инициализация представления админ панели """
    app_admin.add_view(CapitalCityAdmin)
    return app_admin

