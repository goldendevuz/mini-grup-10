# Берем официальный Python. Slim версия меньше весит.
FROM python:3.13-slim

# Чтобы Python не создавал лишние файлы .pyc и сразу выводил логи
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Папка внутри контейнера, где будет лежать наш код
WORKDIR /app

# Устанавливаем зависимости для работы с PostgreSQL (если будешь его юзать)
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Сначала копируем только зависимости, чтобы Docker кэшировал их и не перекачивал каждый раз
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Теперь копируем весь наш код в папку /app
COPY . /app/