from gestfg.celery_app import celery
from celery.utils.log import get_task_logger
import logging
from django.core.mail import send_mail
logger = get_task_logger(__name__)


@celery.task
def send_mail_task(subject, email, DEFAULT_FROM_EMAIL, destiny, fail_silently, auth_user, auth_password):
    from authentication.views import ResetPasswordRequestView
    logger.info('Enviando email por celery')
    send_mail(subject, email, DEFAULT_FROM_EMAIL, destiny, fail_silently, auth_user, auth_password)
