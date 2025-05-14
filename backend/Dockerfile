# Используем официальный образ Python
FROM python:3.11-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Установка gunicorn (для запуска через Nginx)
RUN pip install gunicorn==20.1.0

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install -r requirements.txt --no-cache-dir

# Копируем весь код проекта
COPY . .

# Команда запуска приложения
CMD ["gunicorn", "--bind", "0.0.0.0:9000", "config.wsgi"]