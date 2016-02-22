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

        self.data_alum2 = dict(username='ejemplo2@correo.ugr.es', first_name='alumno 2',
                               last_name='apellido 12 apellido 122')

        self.data_alum_error = dict(username='ejemplo2', first_name='alumno 2',
                                    last_name='apellido 12 apellido 122')

    def test_ws_alumnos_error(self):
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

        # inserto un alumno con parametros incorrectos
        res = requests.post('http://127.0.0.1:8000/alumnos/', data='perico')
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], 'Error en la llamada')

        # inserto un alumno erroneo
        res = requests.post('http://127.0.0.1:8000/alumnos/', data=self.data_alum_error)
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], 'El correo no es correcto')

        # Borrar alumno que no existe
        res = requests.post('http://127.0.0.1:8000/alumnos/delete_alumno/',
                            params={'username': 'pepito'})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], "El alumno indicado no existe")

        # Modificar un alumno que no existe
        res = requests.post('http://127.0.0.1:8000/alumnos/update_alumno/',
                            params={'alumno': 'pepito', 'campos': json.dumps({'first_name': 'otro alumno 2'})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], "El alumno indicado no existe")

    def test_ws_alumnos(self):
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

        # Modificar un alumno con parametros  incorrectos
        res = requests.post('http://127.0.0.1:8000/alumnos/update_alumno/',
                            params={'alumno': 'ejemplo@correo.ugr.es',
                                    'nocampos': json.dumps({'first_name': 'otro alumno 2'})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], "Error en la llamada")

        # Modificar un alumno
        res = requests.post('http://127.0.0.1:8000/alumnos/update_alumno/',
                            data={'alumno': self.data_alum1['username'],
                                  'campos': json.dumps({'first_name': 'otro alumno 1'})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Dejo la BD como estaba
        res = requests.post('http://127.0.0.1:8000/alumnos/delete_alumno/',
                            params={'username': 'ejemplo@correo.ugr.es'})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
