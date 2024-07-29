# Используйте официальный образ Python как основу
FROM python:3.8

# Установите рабочую директорию
WORKDIR /app

# Скопируйте файлы requirements.txt в рабочую директорию
COPY requirements.txt .

# Обновите pip и установите зависимости
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Установите detectron2 отдельно
RUN pip install git+https://github.com/facebookresearch/detectron2.git@94113be6e12db36b8c7601e13747587f19ec92fe

# Скопируйте остальные файлы проекта в рабочую директорию
COPY . .

# Установите переменную окружения для Django
ENV DJANGO_SETTINGS_MODULE=znakapp.settings

# Установите переменную окружения PYTHONPATH для корректного импорта модулей
ENV PYTHONPATH=/app

# Запустите миграции базы данных
RUN python manage.py migrate

# Команда для запуска сервера Django
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "znakapp.asgi:application"]
