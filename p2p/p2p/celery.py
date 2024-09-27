import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "p2p.settings")
app = Celery("p2p_worker")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'cleanup_old_jobs_daily': {
        'task': 'inference.tasks.cleanup_old_jobs',
        'schedule': 86400,  # Every day
    },
}