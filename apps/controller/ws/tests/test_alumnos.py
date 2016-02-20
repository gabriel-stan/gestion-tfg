__author__ = 'tonima'
from django.contrib.auth.models import Group
from django.test import TestCase
from controller.servicios import tfg_services
from model.models import Alumno, Profesor
import requests
import simplejson as json


class TfgServicesTests(TestCase):
    def setUp(self):
        self.data_alum1 = dict(username='ejemplo@correo.ugr.es', first_name='alumno 1',
                               last_name='apellido 1 apellido 12')

        self.prof2_username = 'ejemplo2@ugr.es'
        self.prof2_nombre = 'profesor 2'
        self.prof2_apellidos = 'apellido 2 apellido 22'
        self.prof2_departamento = 'departamento 2'

    def test_get_alumnos_error(self):
        # Sin alumnos
        res = requests.get('http://127.0.0.1:8000/alumnos')
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], 'No hay alumnos almacenados')

        # El alumno no existe
        res = requests.get('http://127.0.0.1:8000/alumnos', params={'username': 'pepito'})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], 'El alumno indicado no existe')

    def test_get_alumnos(self):
        # inserto un alumno
        res = requests.post('http://127.0.0.1:8000/alumnos/', data=self.data_alum1)
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Alumno recien insertado
        res = requests.get('http://127.0.0.1:8000/alumnos', params={'username': 'ejemplo@correo.ugr.es'})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        self.assertEqual(resul['data']['first_name'], 'alumno 1')

        # Todos los alumnos
        res = requests.get('http://127.0.0.1:8000/alumnos')
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        self.assertEqual(resul['data'][0]['first_name'], 'alumno 1')

        # Obtener alumno que no existe
        res = requests.get('http://127.0.0.1:8000/alumnos/', params={'username': 'pepito'})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], "El alumno indicado no existe")

        # Borrar alumno que no existe
        res = requests.post('http://127.0.0.1:8000/alumnos/delete_alumno/',
                            params={'username': 'pepito'})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], "El alumno indicado no existe")

        # Dejo la BD como estaba
        res = requests.post('http://127.0.0.1:8000/alumnos/delete_alumno/',
                            params={'username': 'ejemplo@correo.ugr.es'})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
