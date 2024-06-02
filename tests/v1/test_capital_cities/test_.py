import pytest
from starlette import status


def test_get_status_ok(client, prefix):
    """- получение """
    response = client.get(url=f"{prefix}")
    assert response.status_code == status.HTTP_200_OK


def test_create_data(client, prefix, dct_create_data, coordinates_create, properties_create):
    """- проверить эндпойнт, создания новых данных """
    response = client.post(url=f"{prefix}/create", json=dct_create_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() != {'detail': 'СТРАНА И ГОРОД УЖЕ СУЩЕСТВУЮТ'}

    response_response_geometry = response.json()['features'][0]['geometry']['coordinates']
    response_properties = response.json()['features'][0]['properties']

    assert response_response_geometry[0] == coordinates_create.longitude
    assert response_response_geometry[1] == coordinates_create.latitude
    assert response_properties['country'] == properties_create.country
    assert response_properties['city'] == properties_create.city



def test_check_create_is_duplicated(client, prefix, dct_create_data):
    """- проверить проверка дублирование данных при повторном создании """
    response = client.post(url=f"{prefix}/create", json=dct_create_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'detail': 'СТРАНА И ГОРОД УЖЕ СУЩЕСТВУЮТ'}


def test_new_data_to_db(instance_create, properties_create):
    """- проверка созданных данных на существование в базе """
    assert instance_create.city == properties_create.city and instance_create.country == properties_create.country


def test_get_all(client, prefix, schema_create):
    """- проверка получение всех данных """
    response = client.get(url=f"{prefix}/")
    assert response.status_code == status.HTTP_200_OK
    response_json = response.json()
    assert response_json['type'] == 'FeatureCollection'
    assert len(response_json['features']) != 0


def test_get_one(client, prefix, instance_create, coordinates_create, properties_create):
    """- проверка получение по ID """
    response = client.get(url=f"{prefix}/{instance_create.id}")
    assert response.status_code == status.HTTP_200_OK

    response_json = response.json()
    response_response_geometry = response.json()['features'][0]['geometry']['coordinates']
    response_properties = response.json()['features'][0]['properties']

    assert response_json['type'] == 'FeatureCollection'
    assert len(response_json['features']) != 0
    assert response_response_geometry[0] == coordinates_create.longitude
    assert response_response_geometry[1] == coordinates_create.latitude
    assert response_properties['country'] == properties_create.country
    assert response_properties['city'] == properties_create.city


def test_get_one_not_id(client, prefix, instance_create, schema_create):
    """- проверка ID не существующего ID """
    pk = instance_create.id + 1000
    response = client.get(url=f"{prefix}/{pk}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'ID НЕ НАЙДЕН'}


def test_update(client, prefix, dct_update_data, coordinates_update, properties_update, instance_create):
    """- проверить эндпойнт, обновление новых данных """

    response = client.put(url=f"{prefix}/{instance_create.id}", json=dct_update_data)
    assert response.status_code == status.HTTP_200_OK

    response_json = response.json()

    assert response_json['type'] == 'FeatureCollection'
    assert len(response_json['features']) != 0

    response_response_geometry = response.json()['features'][0]['geometry']['coordinates']
    response_properties = response.json()['features'][0]['properties']

    assert response_response_geometry[0] == coordinates_update.longitude
    assert response_response_geometry[1] == coordinates_update.latitude
    assert response_properties['country'] == properties_update.country
    assert response_properties['city'] == properties_update.city


def test_delete(db, client, prefix, instance_update):
    """- проверка удаления """
    response = client.delete(url=f"{prefix}/{instance_update.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"detail": "ДАННЫЕ УДАЛЕНЫ"}


