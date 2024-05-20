from pprint import pprint

import pytest
from sqlalchemy import select

from src.models import CapitalCity


@pytest.mark.itmo_capital_cities
def test_create_data(client, prefix, dct_data, schema_create):
    """- проверить эндпойнт, создания новых данных """
    response = client.post(url=f"{prefix}/create", json=dct_data)
    assert response.status_code == 200


@pytest.mark.itmo_capital_cities
def test_get_status_ok(client, prefix, dct_data, schema_create):
    """- проверить эндпойнт, создания новых данных """
    response = client.get(url=f"{prefix}")
    assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.itmo_capital_cities
async def test_new_data_to_db(db, client, prefix, dct_data, schema_create):
    """- проверка созданных данных на существование в базе """

    db_execute = await db.execute(select(CapitalCity).where(CapitalCity.city == schema_create.city,
                                                            CapitalCity.country == schema_create.country))
    instance = db_execute.scalars().first()
    assert instance.city == schema_create.city and instance.country == schema_create.country


# def test_get_all(client, prefix):
#     """- проверка получение всех данных """
#     with client.get(url=f"{prefix}/") as response:
#         ...
#
#
# def test_get_one(client, prefix, obj):
#     """- проверка получение по ID """
#     with client.get(url=f"{prefix}/{obj.id}/") as response:
#         ...
#
#
# def test_update(client, prefix, data, obj):
#     """- проверка обновления """
#     with client.put(url=f"{prefix}/{obj.id}", data=data.json()) as response:
#         ...
#
#
# def test_delete(client, prefix, obj):
#     """- проверка удаления """
#     with client.delete(url=f"{prefix}/{obj.id}") as response:
#         ...
