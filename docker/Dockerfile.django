FROM python:3.10

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Устанавливаем обновления и необходимые модули
RUN apt-get update && apt-get install -y binutils libproj-dev gdal-bin
RUN apt install postgis --no-install-recommends
RUN apt-get install python3-gdal

WORKDIR /app

# Обновление pip python
RUN pip install --upgrade pip

# Установка пакетов для проекта
COPY requirements.txt .

#RUN pip install -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . .

## Настройка записи и доступа
#RUN chmod -R 777 ./