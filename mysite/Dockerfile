FROM python:3.11-slim

WORKDIR /app

# Установка Poetry
RUN pip install poetry

# Отключаем создание виртуального окружения внутри Docker
RUN poetry config virtualenvs.create false

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock* /app/

# Устанавливаем зависимости
RUN poetry install --no-dev --no-interaction --no-ansi

# Копируем код приложения
COPY . .

# Команда запуска
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]