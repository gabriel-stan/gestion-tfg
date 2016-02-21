__author__ = 'tonima'
from django.contrib.auth.models import Group
from django.test import TestCase
from controller.servicios import tfg_services
from model.models import Profesor
import requests
import simplejson as json


class TfgServicesTests(TestCase):
    def setUp(self):
        self.data_prof1 = dict(username='prof_ejemplo@ugr.es', first_name='profesor 1',
                               last_name='apellido 1 apellido 12', departamento='el mas mejor')

        self.data_prof2 = dict(username='prof_ejemplo2@ugr.es', first_name='profesor 2',
                               last_name='apellido 12 apellido 122', departamento='el mas mejor')

        self.data_prof_error = dict(username='prof_ejemplo2', first_name='profesor 2',
                                    last_name='apellido 12 apellido 122', departamento='el mas mejor')


    def test_ws_profesors_error(self):
        # Sin profesors
        res = requests.get('http://127.0.0.1:8000/profesores')
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], 'No hay profesores almacenados')

        # El profesor no existe
        res = requests.get('http://127.0.0.1:8000/profesores', params={'username': 'pepito'})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], 'El profesor indicado no existe')

        # inserto un profesor con parametros incorrectos
        res = requests.post('http://127.0.0.1:8000/profesores/', data='perico')
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], 'Error en la llamada')

        # inserto un profesor erroneo
        res = requests.post('http://127.0.0.1:8000/profesores/', data=self.data_prof_error)
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], 'El correo no es correcto')

        # Obtener profesor que no existe
        res = requests.get('http://127.0.0.1:8000/profesores/', params={'username': 'pepito'})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], "El profesor indicado no existe")

        # Borrar profesor que no existe
        res = requests.post('http://127.0.0.1:8000/profesores/delete_profesor/',
                            params={'username': 'pepito'})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], "El profesor indicado no existe")

        # Modificar un profesor que no existe
        res = requests.post('http://127.0.0.1:8000/profesores/update_profesor/',
                            params={'profesor': 'pepito', 'campos': json.dumps({'first_name': 'otro profesor 2'})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], "El profesor indicado no existe")

    def test_ws_profesors(self):
        # inserto un profesor
        res = requests.post('http://127.0.0.1:8000/profesores/', data=self.data_prof1)
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # profesor recien insertado
        res = requests.get('http://127.0.0.1:8000/profesores', params={'username': self.data_prof1['username']})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        self.assertEqual(resul['data']['first_name'], self.data_prof1['first_name'])

        # Todos los profesors
        res = requests.get('http://127.0.0.1:8000/profesores')
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        self.assertEqual(resul['data'][0]['first_name'], 'profesor 1')

        # Modificar un profesor con parametros incorrectos
        res = requests.post('http://127.0.0.1:8000/profesores/update_profesor/',
                            params={'profesor': self.data_prof1['username'],
                                    'nocampos': json.dumps({'first_name': 'otro profesor 2'})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], "Error en la llamada")

        # Modificar un profesor
        res = requests.post('http://127.0.0.1:8000/profesores/update_profesor/',
                            data={'profesor': self.data_prof1['username'],
                                  'campos': json.dumps({'first_name': 'otro profesor 1'})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Dejo la BD como estaba
        res = requests.post('http://127.0.0.1:8000/profesores/delete_profesor/',
                            params={'username': self.data_prof1['username']})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
