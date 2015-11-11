"""
WSGI config for gestion_tfg project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

#import for Heroku deployment
from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gestion_tfg.settings")

application = get_wsgi_application()

# Heroku static files management
application = DjangoWhiteNoise(application)