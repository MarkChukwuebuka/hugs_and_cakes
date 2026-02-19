from __future__ import absolute_import

import os

from celery import Celery
from django.apps import apps
from django.conf import settings
from kombu import Queue

# --> celery -A core worker -l info -Q default -c 4 -n default@%h
# --> celery -A core worker -l info -Q logging -c 1 -n logging@%h
# --> celery -A core worker -l info -Q email -c 4 -n email@%h
# --> celery -A core beat -l info

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core", broker=settings.BROKER_URL)

app.config_from_object("django.conf:settings", namespace="CELERY")

# ---- queues ----
app.conf.task_queues = (
    Queue("email"),
    Queue("logging"),
    Queue("default"),
)

app.conf.task_default_queue = "default"
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
