import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gestfg.settings")
from django.contrib.auth import get_user_model
User = get_user_model()

try:
    auth_models.User.objects.get(username='admin')
except auth_models.User.DoesNotExist:
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
