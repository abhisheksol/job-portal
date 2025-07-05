# smart_hiring/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_hiring.settings')

app = Celery('smart_hiring')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
