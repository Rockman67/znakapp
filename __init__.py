import os
import sys
from pathlib import Path

# Установите базовый путь проекта
BASE_DIR = Path(__file__).resolve().parent

# Добавьте базовый путь проекта в sys.path
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# Импортируйте и настройте celery
from znakapp.celery_app import app as celery_app

__all__ = ('celery_app',)
