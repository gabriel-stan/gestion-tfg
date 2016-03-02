__author__ = 'tonima'
from django.contrib.auth.models import Group
from django.test import TestCase
from controller.servicios import tfg_services
from model.models import Alumno, Profesor
import simplejson as json
from rest_framework.test import APIClient


class TfgServicesTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.data_alum1 = dict(username='ejemplo@correo.ugr.es', first_name='alumno 1',
                               last_name='apellido 1 apellido 12')

        self.data_alum2 = dict(username='ejemplo2@correo.ugr.es', first_name='alumno 2',
                               last_name='apellido 12 apellido 122')

        self.data_alum_error = dict(username='ejemplo2', first_name='alumno 2',
                                    last_name='apellido 12 apellido 122')

    def test_ws_alumnos_error(self):
        # Sin alumnos
        res = self.client.get('/alumnos/')
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], 'No hay alumnos almacenados')

        # El alumno no existe
        res = self.client.get('/alumnos/',  {'username': 'pepito'})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], 'El alumno indicado no existe')

        # inserto un alumno erroneo
        res = self.client.post('/alumnos/', self.data_alum_error)
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], 'El correo no es correcto')

        # Borrar alumno que no existe
        res = self.client.post('/alumnos/delete_alumno/',
                             {'username': 'pepito'})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], "El alumno indicado no existe")

        # Modificar un alumno que no existe
        res = self.client.post('/alumnos/update_alumno/',
                             {'alumno': 'pepito', 'campos': json.dumps({'first_name': 'otro alumno 2'})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], "El alumno indicado no existe")

    def test_ws_alumnos(self):
        # inserto un alumno
        res = self.client.post('/alumnos/', self.data_alum1)
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Alumno recien insertado
        res = self.client.get('/alumnos/',  {'username': 'ejemplo@correo.ugr.es'})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        self.assertEqual(resul['data']['first_name'], 'alumno 1')

        # Todos los alumnos
        res = self.client.get('/alumnos/')
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        self.assertEqual(resul['data'][0]['first_name'], 'alumno 1')

        # Modificar un alumno con parametros  incorrectos
        res = self.client.post('/alumnos/update_alumno/',
                             {'alumno': 'ejemplo@correo.ugr.es',
                                    'nocampos': json.dumps({'first_name': 'otro alumno 2'})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], "Error en la llamada")

        # Modificar un alumno
        res = self.client.post('/alumnos/update_alumno/',
                            {'alumno': self.data_alum1['username'],
                                  'campos': json.dumps({'first_name': 'otro alumno 1'})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Dejo la BD como estaba
        res = self.client.post('/alumnos/delete_alumno/',
                             {'username': 'ejemplo@correo.ugr.es'})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
