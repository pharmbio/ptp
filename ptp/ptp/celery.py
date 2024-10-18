import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ptp.settings")
app = Celery("ptp_worker")
app.config_from_object("ptp.settings", namespace="CELERY")
from django.apps import apps
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'cleanup_old_jobs_daily': {
        'task': 'inference.tasks.cleanup_old_jobs',
        'schedule': 86400,  # Every day
    },
}