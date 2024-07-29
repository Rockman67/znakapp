from __future__ import absolute_import, unicode_literals
import os
import sys
from pathlib import Path

# Добавьте путь к проекту в sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from celery import Celery
from django.conf import settings

# Установите модуль настроек Django по умолчанию для программы Celery.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'znakapp.settings')

app = Celery('znakapp')

# Используйте строку настроек в виде конфигурации по умолчанию с префиксом `CELERY`.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживайте задачи в ваших приложениях Django.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
