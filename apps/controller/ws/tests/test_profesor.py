__author__ = 'tonima'
from django.contrib.auth.models import Group
from django.test import TestCase
from controller.servicios import tfg_services
from model.models import Profesor
import simplejson as json
from rest_framework.test import APIClient


class TfgServicesTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.data_prof1 = dict(username='prof_ejemplo@ugr.es', first_name='profesor 1',
                               last_name='apellido 1 apellido 12', departamento='el mas mejor', password='1234')

        self.data_prof2 = dict(username='prof_ejemplo2@ugr.es', first_name='profesor 2',
                               last_name='apellido 12 apellido 122', departamento='el mas mejor', password='1234')

        self.data_prof_error = dict(username='prof_ejemplo2', first_name='profesor 2',
                                    last_name='apellido 12 apellido 122', departamento='el mas mejor', password='1234')

    def test_ws_profesors_error(self):
        # Sin profesors
        res = self.client.get('/profesores/')
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], 'No hay profesores almacenados')

        # El profesor no existe
        res = self.client.get('/profesores/', {'username': 'pepito'})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], 'El profesor indicado no existe')

        # inserto un profesor erroneo
        res = self.client.post('/profesores/', self.data_prof_error)
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], 'El correo no es correcto')

        # Borrar profesor que no existe
        res = self.client.post('/profesores/delete_profesor/',
                            {'username': 'pepito'})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], "El profesor indicado no existe")

        # Modificar un profesor que no existe
        res = self.client.post('/profesores/update_profesor/',
                            {'profesor': 'pepito', 'campos': json.dumps({'first_name': 'otro profesor 2'})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], "El profesor indicado no existe")

    def test_ws_profesors(self):
        # inserto un profesor
        res = self.client.post('/profesores/', self.data_prof1)
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # profesor recien insertado
        res = self.client.get('/profesores/', {'username': self.data_prof1['username']})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        self.assertEqual(resul['data']['first_name'], self.data_prof1['first_name'])

        # Todos los profesors
        res = self.client.get('/profesores/')
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        self.assertEqual(resul['data'][0]['first_name'], 'profesor 1')

        # Modificar un profesor con parametros incorrectos
        res = self.client.post('/profesores/update_profesor/',
                            {'profesor': self.data_prof1['username'],
                                    'nocampos': json.dumps({'first_name': 'otro profesor 2'})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], "Error en la llamada")

        # Modificar un profesor
        res = self.client.post('/profesores/update_profesor/',
                            {'profesor': self.data_prof1['username'],
                                  'campos': json.dumps({'first_name': 'otro profesor 1'})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        # self.assertEqual(resul['data']['first_name'], 'otro profesor 1')

        # Dejo la BD como estaba
        res = self.client.post('/profesores/delete_profesor/',
                            {'username': self.data_prof1['username']})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
