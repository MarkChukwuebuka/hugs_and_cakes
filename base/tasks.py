from django.conf import settings

from base.models import Activity, ApiRequestLogger
from core.celery import app



@app.task
def report_activity(user, activity_type, description):
    Activity.objects.create(user=user, activity_type=activity_type, note=description)
