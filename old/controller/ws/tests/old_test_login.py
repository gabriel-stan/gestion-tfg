__author__ = 'tonima'
from django.contrib.auth.models import Group
from django.test import TestCase
import simplejson as json
from rest_framework.test import APIClient

from model.models import Profesor


class TfgServicesTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.grupo_profesores = Group.objects.get(name='Profesores')

        self.data_alum1 = dict(username='ejemplo@correo.ugr.es', first_name='alumno 1',
                                 last_name='apellido 1 apellido 12', password='75169052')

        self.data_login = Profesor(username='ejemplo3@ugr.es', first_name='profesor 1',
                               last_name='apellido 1 apellido 12', departamento='el mas mejor', password='75169052')

        self.data_login.save()
        self.grupo_profesores.user_set.add(self.data_login)

    def test_ws_alumnos_error(self):
        # inserto un alumno
        res = self.client.login(username='ejemplo3@ugr.es', password='75169052')
        self.assertEqual(res, True)
        res = self.client.post('/alumnos/', self.data_alum1)
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
