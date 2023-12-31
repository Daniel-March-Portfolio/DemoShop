import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DemoShop.settings")

app = Celery("DemoShop")
app.config_from_object("django.conf:settings")
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'create_payment_intents': {
        'task': 'Payment.tasks.create_payment_intents',
        'schedule': crontab(minute="*"),
    },
}
