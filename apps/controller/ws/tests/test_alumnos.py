__author__ = 'tonima'
from django.contrib.auth.models import Group
from django.test import TestCase
from controller.servicios import tfg_services
from model.models import Alumno, Profesor
import requests
import simplejson as json

class TfgServicesTests(TestCase):
    def test_get_alumnos_error(self):
        # El alumnos no existe
        res = requests.get('http://127.0.0.1:8000/alumnos')
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)

