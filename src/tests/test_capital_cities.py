

def test_create(client, prefix, data):
    """- проверка создания """
    with client.post(f"{prefix}/create", data=data.json()) as response:
        ...


def test_get_all(client, prefix):
    """- проверка получение всех данных """
    with client.get(prefix) as response:
        ...


def test_get_one(client, prefix, obj):
    """- проверка получение по ID """
    with client.get(f"{prefix}/{obj.id}/") as response:
        ...


def test_update(client, prefix, data, obj):
    """- проверка обновления """
    with client.put(f"{prefix}/{obj.id}", data=data.json()) as response:
        ...


def test_delete(client, prefix, obj):
    """- проверка удаления """
    with client.delete(f"{prefix}/{obj.id}") as response:
        ...
