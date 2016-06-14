# -*- coding: utf-8 -*-
from django.test import TestCase
from rest_framework.test import APIClient
from authentication.models import Usuario, Departamento
from django.contrib.auth.models import Group
import simplejson as json
import os


class AuthenticationServicesTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.data_admin = dict(dni='75169052S', first_name='admin 1',
                               last_name='apellido 1 apellido 12', password='0000', is_admin=True)
        Usuario.objects.create_superuser(**self.data_admin)

        self.data_admin2 = dict(email='admin2@admin.es', first_name='admin 2',
                               last_name='apellido 1 apellido 12', password='0000', is_admin=True)

        self.data_alum1 = dict(dni='12345678H', first_name='alumno 1',
                               last_name='apellido 1 apellido 12', password='0000')

        self.data_alum2 = dict(email='ejemplo2@correo.ugr.es', first_name='alumno 2',
                               last_name='apellido 12 apellido 122', password='0000')

        self.data_alum_error = dict(email='ejemplo2', first_name='alumno 2',
                                    last_name='apellido 12 apellido 122', password='0000')

        dep = Departamento.objects.create(nombre='departamento1', codigo='AAA')

        self.data_prof1 = dict(dni='87654321S', first_name='profesor 2',
                                    last_name='apellido 12 apellido 122', departamento=dep, password='0000')

        self.data_departamento = dict(codigo='BBB', nombre='departamento2')

    def test_ws_alumnos_get(self):
        # Sin alumnos
        res = self.client.get('/api/v1/alumnos/', self.data_alum1)
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], 'El alumno indicado no existe')
        res = self.client.get('/api/v1/alumnos/')
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], 'No hay alumnos almacenados')

    def test_ws_alumnos_post(self):

        # inserto un alumno
        res = self.client.post('/api/v1/alumnos/', self.data_alum1)
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Modificar un alumno
        res = self.client.post('/api/v1/auth/login/', dict(dni=self.data_alum1['dni'],
                                                           password=self.data_alum1['password']))
        res = self.client.put('/api/v1/alumnos/', {'usuario': self.data_alum1['dni'],
                                                   'datos': json.dumps({'first_name': 'otro alumno 2'})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

    def test_ws_alumnos_delete(self):

        # inserto un alumno
        res = self.client.post('/api/v1/alumnos/', self.data_alum1)
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Login con un administrador
        res = self.client.post('/api/v1/auth/login/', dict(dni=self.data_admin['dni'],
                                                           password=self.data_admin['password']))

         # elimino el alumno
        res = self.client.delete('/api/v1/alumnos/', self.data_alum1)
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

    def test_ws_profesores_get(self):
        # inserto un profesor
        res = self.client.post('/api/v1/profesores/', self.data_prof1)
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Me logueo con un profesor
        res = self.client.post('/api/v1/auth/login/', {'dni': self.data_prof1['dni'],
                                                       'password': self.data_prof1['password']})
        resul = json.loads(res.content)
        self.assertEqual(resul['data']['dni'], self.data_prof1['dni'])
        # Modificar un profesor
        res = self.client.put('/api/v1/profesores/', {'usuario': self.data_prof1['dni'],
                                                      'datos': json.dumps({'first_name': 'otro profesor 2'})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Introduzco 2 alumnos
        res = self.client.post('/api/v1/alumnos/', self.data_alum1)
        res = self.client.post('/api/v1/alumnos/', self.data_alum2)
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Me logueo con un admin
        res = self.client.post('/api/v1/auth/login/', {'dni': self.data_prof1['dni'],
                                                       'password': self.data_prof1['password']})
        resul = json.loads(res.content)
        self.assertEqual(resul['data']['dni'], self.data_prof1['dni'])

        # obtengo todos los usuarios pero sin dni por que soy un profesor
        res = self.client.get('/api/v1/usuarios/')
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        self.assertEqual(resul['data'][0].get('dni'), None)
        #self.assertEqual(resul['data'][0].get('clase'), 'Alumno')

        # Me logueo con un admin
        res = self.client.post('/api/v1/auth/login/', {'dni': self.data_admin['dni'],
                                                       'password': self.data_admin['password']})
        resul = json.loads(res.content)
        self.assertEqual(resul['data']['dni'], self.data_admin['dni'])

    def test_ws_usuarios_get(self):
        # Me logueo con un admin
        res = self.client.post('/api/v1/auth/login/', {'dni': self.data_admin['dni'],
                                                       'password': self.data_admin['password']})
        resul = json.loads(res.content)
        self.assertEqual(resul['data']['dni'], self.data_admin['dni'])

        # Introduzco 2 usuarios
        res = self.client.post('/api/v1/profesores/', self.data_prof1)
        res = self.client.post('/api/v1/alumnos/', self.data_alum2)
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # obtengo todos los alumnos por que soy un profesor
        res = self.client.get('/api/v1/usuarios/')
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

    def test_ws_admins_get(self):
        # Me logueo con un admin
        res = self.client.post('/api/v1/auth/login/', {'dni': self.data_admin['dni'],
                                                       'password': self.data_admin['password']})
        resul = json.loads(res.content)
        self.assertEqual(resul['data']['dni'], self.data_admin['dni'])

        # Creo otro admin
        res = self.client.post('/api/v1/usuarios/', self.data_admin2)
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

    def test_ws_permisos_get(self):
        # inserto un profesor
        res = self.client.post('/api/v1/profesores/', self.data_prof1)
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        # Me logueo con un profesor
        res = self.client.post('/api/v1/auth/login/', {'dni': self.data_prof1['dni'],
                                                       'password': self.data_prof1['password']})
        resul = json.loads(res.content)
        self.assertEqual(resul['data']['dni'], self.data_prof1['dni'])
        # Me logueo con un profesor
        res = self.client.get('/api/v1/auth/permisos/')
        resul = json.loads(res.content)
        self.assertEqual(resul['permissions']['evento'][0], 'change')

    def test_ws_permisos_post(self):
        # inserto un profesor
        res = self.client.post('/api/v1/profesores/', self.data_prof1)
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        # Me logueo con un profesor
        res = self.client.post('/api/v1/auth/login/', {'dni': self.data_prof1['dni'],
                                                       'password': self.data_prof1['password']})
        resul = json.loads(res.content)
        self.assertEqual(resul['data']['dni'], self.data_prof1['dni'])
        # Me logueo con un profesor
        res = self.client.get('/api/v1/auth/permisos/')
        resul = json.loads(res.content)
        self.assertEqual(resul['permissions']['evento'][0], 'change')

    def test_load_data(self):
        # Me logueo con un admin
        res = self.client.post('/api/v1/auth/login/', {'dni': self.data_admin['dni'],
                                                       'password': self.data_admin['password']})
        resul = json.loads(res.content)
        self.assertEqual(resul['data']['dni'], self.data_admin['dni'])

        location = os.path.join(os.path.dirname(__file__), 'test_load_data', 'LoadDepartamentos.csv')
        data = {'file': ('LoadDepartamentos.csv', open(location, 'rb')), 'model': 'departamento'}
        res = self.client.post('/api/v1/auth/load_data/', data, format='multipart')
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

    def test_departamento(self):
        # Me logueo con un admin
        res = self.client.post('/api/v1/auth/login/', {'dni': self.data_admin['dni'],
                                                       'password': self.data_admin['password']})
        resul = json.loads(res.content)
        self.assertEqual(resul['data']['dni'], self.data_admin['dni'])

        res = self.client.post('/api/v1/auth/departamentos/', {'codigo': self.data_departamento['codigo'],
                                                               'nombre': self.data_departamento['nombre']})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        res = self.client.put('/api/v1/auth/departamentos/', {'codigo': self.data_departamento['codigo'],
                                                              'data': json.dumps(
                                                                  {'nombre': 'departamento chulo'})})
        resul = json.loads(res.content)
        self.assertEqual(resul['data']['nombre'], 'departamento chulo')

        res = self.client.get('/api/v1/auth/departamentos/')
        resul = json.loads(res.content)
        self.assertEqual(resul['data'][1]['nombre'], 'departamento chulo')

