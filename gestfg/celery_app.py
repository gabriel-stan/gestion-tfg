from celery import Celery
from gestfg import settings
import os
import redis

try:
    from settings import HOST_REDIS
except ImportError:
    HOST_REDIS = 'localhost'
try:
    from settings import PUERTO_CELERY
except ImportError:
    PUERTO_CELERY = '0'

celery = Celery(broker='redis://localhost:6379/%s' % PUERTO_CELERY,
                backend='redis://localhost:6379/%s' % PUERTO_CELERY,
                include=['gestfg.tasks'])

# Optional configuration, see the application user guide.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestfg.settings')
celery.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
    BROKER_TRANSPORT_OPTIONS={'visibility_timeout': 365 * 24 * 60 * 60}, #365 * 24 * 60 * 60
)