# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from gestfg.settings import EMAIL_HOST_USER
import const_mensajes
from gestfg.tasks import send_mail_task


def email_asig_tfg(tfg, usuarios):
    a =const_mensajes.MENSAJE_ASIG_TFG.format(titulo=tfg)
    send_mail_task.delay(u'[GESTFG] - Notificación de Asignación', const_mensajes.MENSAJE_ASIG_TFG.format(titulo=tfg), EMAIL_HOST_USER, usuarios)
