FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
# НЕТ SECRET_KEY в Dockerfile!

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p staticfiles uploads

# Безопасный collectstatic с временным ключом
RUN COLLECTSTATIC=1 python manage.py collectstatic --noinput

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "mysite.wsgi:application"]