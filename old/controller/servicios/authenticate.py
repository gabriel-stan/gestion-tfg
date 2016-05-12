__author__ = 'tonima'
from django.contrib.auth.models import User
from authentication.models import Alumno, Profesor


class Authentication(object):

    def authenticate(self, email=None, password=None):
         try:
             o = Alumno.objects.get(email=email, password=password)
             return Alumno.objects.get(email=o.email)
         except Alumno.DoesNotExist:
             try:
                 o = Profesor.objects.get(email=email, password=password)
                 return Profesor.objects.get(email=o.email)
             except Profesor.DoesNotExist:
                 return None

    def get_user(self, user_id):
       try:
          return Alumno.objects.get(pk=user_id)
       except Alumno.DoesNotExist:
             try:
                 return Profesor.objects.get(pk=user_id)
             except Profesor.DoesNotExist:
                 return None