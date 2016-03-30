__author__ = 'tonima'
from django.contrib.auth.models import User
from model.models import Alumno, Profesor


class Authentication(object):

    def authenticate(self, username=None, password=None):
         try:
             o = Alumno.objects.get(username=username, password=password)
             return Alumno.objects.get(username=o.username)
         except Alumno.DoesNotExist:
             try:
                 o = Profesor.objects.get(username=username, password=password)
                 return Profesor.objects.get(username=o.username)
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