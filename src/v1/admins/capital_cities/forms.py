import wtforms
from wtforms.validators import ValidationError, DataRequired, Length


def validate_is_instance_to_string(form, field):
    """- проверка валидности поля на строчный тип данных """
    if not str(field.data).isalpha():
        raise ValidationError('Поле должно быть заполнено только строчным типом.')


validate_create_capital_city = [DataRequired(), Length(min=2, max=100), validate_is_instance_to_string]


class CreateCapitalCityAdminForm(wtforms.Form):
    """- форма создания столицы городов """
    country = wtforms.StringField("Страна", render_kw={"class": "form-control"}, validators=validate_create_capital_city)
    city = wtforms.StringField("Города", render_kw={"class": "form-control"}, validators=validate_create_capital_city)
    longitude = wtforms.DecimalField("Долгота", render_kw={"class": "form-control"})
    latitude = wtforms.DecimalField("Широта", render_kw={"class": "form-control"})

    class Meta:
        locales = ['ru_RU', 'ru']


