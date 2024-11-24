import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'extract_audio.settings')

celery_app = Celery('extract_audio', broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")

celery_app.config_from_object('django.conf:settings', namespace='CELERY')

celery_app.autodiscover_tasks()

