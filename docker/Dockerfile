FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Обновление pip python
RUN pip install --upgrade pip

# Установка пакетов для проекта
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . .
