# Habit Tracker API

## Описание проекта

Этот проект представляет собой API для отслеживания привычек, который позволяет пользователям создавать, редактировать и
удалять свои привычки, а также получать напоминания через Telegram. API предоставляет возможность работать с полезными и
приятными привычками, а также управлять их периодичностью и вознаграждениями.

## Документация

- **GET /swagger/**: Документация в формате Swagger UI.
- **GET /redoc/**: Документация в формате ReDoc.

## Используемые технологии:

    Python 3.12
    Django 4.2.2
    PostgreSQL
    Django REST Framework
    Celery
    Redis
    Telegram API
    Docker
    Docker Compose

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Tatyana-Kavardaeva/HabitTracker

2. Установите зависимости с помощью Poetry:
    ```bash
    poetry install

3. Настройте переменные окружения.
   Создайте файл .env и добавьте необходимые переменные, такие как:
   ```bash
   SECRET_KEY
   LOCATION
   LOCALHOST
   TELEGRAM_TOKEN
   
   для подключения базы данных:
   NAME
   USER
   PASSWORD

4. Убедитесь, что у вас установлен Docker и Docker Compose.
   Затем выполните:
   ``` bash
   docker-compose up --build

Это создаст и запустит контейнеры для приложения, базы данных, Celery и Redis.
