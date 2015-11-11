"""
WSGI config for gestion_tfg project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gestion_tfg.settings")

#import for Heroku deployment !!!! after setting DJANGO_SETTINGS_MODULE variable!!!
from whitenoise.django import DjangoWhiteNoise

application = get_wsgi_application()

# Heroku static files management
application = DjangoWhiteNoise(application)
