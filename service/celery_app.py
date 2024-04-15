import os
import time

from celery import Celery
from celery.utils.log import get_task_logger

# Setting the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service.settings')

app = Celery('service')

# Using a Django settings module as the configuration source.
app.config_from_object('django.conf.settings', namespace='CELERY')

# This line will tell Celery to auto-discover all your tasks located in your apps listed in INSTALLED_APPS.
app.autodiscover_tasks()

logger = get_task_logger(__name__)


@app.task
def debug_task():
    time.sleep(20)
    print(f"Hello from debug")
