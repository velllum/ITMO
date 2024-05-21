from pprint import pprint

import pytest
from starlette import status


@pytest.mark.itmo_capital_cities
def test_get_status_ok(client, prefix):
    """- получение """
    response = client.get(url=f"{prefix}")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.itmo_capital_cities
def test_create_data(client, prefix, dct_create_data, schema_create):
    """- проверить эндпойнт, создания новых данных """
    response = client.post(url=f"{prefix}/create", json=dct_create_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() != {'detail': 'СТРАНА И ГОРОД УЖЕ СУЩЕСТВУЮТ'}

    response_json = response.json()['features'][0]['geometry']
    schema_create_json = schema_create.model_dump()['geom']['features'][0]['geometry']

    assert response_json['coordinates'][0] == schema_create_json['coordinates'][0]
    assert response_json['coordinates'][1] == schema_create_json['coordinates'][1]
    assert response_json['type'] == schema_create_json['type']


@pytest.mark.itmo_capital_cities
def test_check_create_is_duplicated(client, prefix, dct_create_data):
    """- проверить проверка дублирование данных при повторном создании """
    response = client.post(url=f"{prefix}/create", json=dct_create_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'detail': 'СТРАНА И ГОРОД УЖЕ СУЩЕСТВУЮТ'}


@pytest.mark.itmo_capital_cities
def test_new_data_to_db(instance_create, schema_create):
    """- проверка созданных данных на существование в базе """
    assert instance_create.city == schema_create.city and instance_create.country == schema_create.country


def test_get_all(client, prefix, schema_create):
    """- проверка получение всех данных """
    response = client.get(url=f"{prefix}/")
    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert response_json['type'] == 'FeatureCollection'
    assert len(response_json['features']) != 0


def test_get_one(client, prefix, instance_create, schema_create):
    """- проверка получение по ID """
    response = client.get(url=f"{prefix}/{instance_create.id}")
    assert response.status_code == status.HTTP_200_OK

    response_json = response.json()

    assert response_json['type'] == 'FeatureCollection'
    assert len(response_json['features']) != 0

    response_json = response.json()['features'][0]['geometry']
    schema_create_json = schema_create.model_dump()['geom']['features'][0]['geometry']

    assert response_json['coordinates'][0] == schema_create_json['coordinates'][0]
    assert response_json['coordinates'][1] == schema_create_json['coordinates'][1]
    assert response_json['type'] == schema_create_json['type']

    response_json = response.json()['features'][0]['properties']
    schema_create_json = schema_create.model_dump()

    assert response_json['city'] == schema_create_json['city']
    assert response_json['country'] == schema_create_json['country']


def test_get_one_not_id(client, prefix, instance_create, schema_create):
    """- проверка ID не существующего ID """
    pk = instance_create.id + 1000
    response = client.get(url=f"{prefix}/{pk}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'ID НЕ НАЙДЕН'}


@pytest.mark.itmo_capital_cities
def test_update(client, prefix, dct_update_data, schema_update, instance_create):
    """- проверить эндпойнт, обновление новых данных """

    response = client.put(url=f"{prefix}/{instance_create.id}", json=dct_update_data)
    assert response.status_code == status.HTTP_200_OK

    response_json = response.json()['features'][0]['geometry']
    schema_create_json = schema_update.model_dump()['geom']['features'][0]['geometry']

    assert response_json['coordinates'][0] == schema_create_json['coordinates'][0]
    assert response_json['coordinates'][1] == schema_create_json['coordinates'][1]
    assert response_json['type'] == schema_create_json['type']


def test_delete(db, client, prefix, instance_update):
    """- проверка удаления """
    response = client.delete(url=f"{prefix}/{instance_update.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"detail": "ДАННЫЕ УДАЛЕНЫ"}


