## Простой REST-сервис на FastAPI, для работы с геоданными (GeoJson, PostGis).

1. сделать базу, с табличкой хранящей столицы (наполнить, например, бывшими респбликами СССР). 
Название страны, Название города, геометрия (можно точку, можно полигон) 
СУБД Postgresql + PostGIS(https://postgis.net/docs/ST_GeometryType.html)
2. сделать сервис, реализующий CRUD. Получение одной/всех записей из БД, запись, обновление и удаление по одному объекту.
3. ожидаемый ответ на гет запрос - валидный geojson. (проверить можно на geojson.io),
на запись/обновление тело запроса тоже содержащее geojson.
4. результат: код и образ для сборки докер контейнера.

желательно FastAPI, SQLAlchemy 

### Команды

Команда на сборку через Docker - `docker-compose up --build` запустить и собрать
если надо запусть проекта локальн, то в файле settings.py (настройки приложения), закомментировать строку

`model_config = SettingsConfigDict(env_file='./docker/env/prod/.env.web')` и раскомментить 

`model_config = SettingsConfigDict(env_file='./docker/env/dev/.env')`

Приложение запускает по следующим хостам 127.0.0.1, localhost, порт :8000 (Для uvicorn), :8080 (для NGINX).

`python -m src.main_capital_cities` - запуск с локальной машины, из корневой директории ./ITMO

Не забываем установить библиотеки
`pip install -r requirements.txt`

### API

Формат тела для обновления, добавления:

```{
  "country": "<Страна>",
  "city": "<Город>",
  "geom": { // geojson
      "type": "FeatureCollection",
      "features": [
        {
          "type": "Feature",
          "properties": {},
          "geometry": {
            "coordinates": [
              37.19468932272076,
              55.99746473459453
            ],
            "type": "Point"
          }
        }
      ]
    }
}
```

