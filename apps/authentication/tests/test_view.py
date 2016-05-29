# -*- coding: utf-8 -*-
from django.test import TestCase
from rest_framework.test import APIClient
from authentication.models import Usuario
from django.contrib.auth.models import Group
import simplejson as json


class AuthenticationServicesTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.data_admin = dict(email='admin@admin.es', first_name='admin 1',
                               last_name='apellido 1 apellido 12', password='0000', is_admin=True)
        Usuario.objects.create_superuser(**self.data_admin)

        self.data_admin2 = dict(email='admin2@admin.es', first_name='admin 2',
                               last_name='apellido 1 apellido 12', password='0000', is_admin=True)

        self.data_alum1 = dict(email='ejemplo@correo.ugr.es', first_name='alumno 1',
                               last_name='apellido 1 apellido 12', password='0000')

        self.data_alum2 = dict(email='ejemplo2@correo.ugr.es', first_name='alumno 2',
                               last_name='apellido 12 apellido 122', password='0000')

        self.data_alum_error = dict(email='ejemplo2', first_name='alumno 2',
                                    last_name='apellido 12 apellido 122', password='0000')

        self.data_prof1 = dict(email='ejemploprof2@ugr.es', first_name='profesor 2',
                                    last_name='apellido 12 apellido 122', departamento='departamento1', password='0000')

    def test_ws_alumnos_get(self):
        # Sin alumnos
        # res = self.client.login(username='ejemplo3@ugr.es', password='75169052')
        # self.assertEqual(res, True)
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
        res = self.client.post('/api/v1/auth/login/', dict(email=self.data_alum1['email'],
                                                           password=self.data_alum1['password']))
        res = self.client.put('/api/v1/alumnos/', {'alumno': self.data_alum1['email'],
                                                   'datos': json.dumps({'first_name': 'otro alumno 2'})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

    def test_ws_alumnos_delete(self):

        # inserto un alumno
        res = self.client.post('/api/v1/alumnos/', self.data_alum1)
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Login con un administrador
        res = self.client.post('/api/v1/auth/login/', dict(email=self.data_admin['email'],
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
        res = self.client.post('/api/v1/auth/login/', {'email': self.data_prof1['email'], 'password': self.data_prof1['password']})
        resul = json.loads(res.content)
        self.assertEqual(resul['data']['email'], self.data_prof1['email'])
        # Modificar un profesor
        res = self.client.put('/api/v1/profesores/', {'profesor': self.data_prof1['email'], 'datos': json.dumps({'first_name': 'otro profesor 2'})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Introduzco 2 alumnos
        res = self.client.post('/api/v1/alumnos/', self.data_alum1)
        res = self.client.post('/api/v1/alumnos/', self.data_alum2)
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # obtengo todos los alumnos por que soy un profesor
        res = self.client.get('/api/v1/alumnos/')
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

    def test_ws_usuarios_get(self):
        # Me logueo con un admin
        res = self.client.post('/api/v1/auth/login/', {'email': self.data_admin['email'],
                                                       'password': self.data_admin['password']})
        resul = json.loads(res.content)
        self.assertEqual(resul['data']['email'], self.data_admin['email'])

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
        res = self.client.post('/api/v1/auth/login/', {'email': self.data_admin['email'],
                                                       'password': self.data_admin['password']})
        resul = json.loads(res.content)
        self.assertEqual(resul['data']['email'], self.data_admin['email'])

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
        res = self.client.post('/api/v1/auth/login/', {'email': self.data_prof1['email'], 'password': self.data_prof1['password']})
        resul = json.loads(res.content)
        self.assertEqual(resul['data']['email'], self.data_prof1['email'])
        # Me logueo con un profesor
        res = self.client.get('/api/v1/auth/permisos/')
        resul = json.loads(res.content)
        self.assertEqual(resul['permissions'][0]['evento'], 'create')

    def test_ws_permisos_post(self):
        # inserto un profesor
        res = self.client.post('/api/v1/profesores/', self.data_prof1)
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        # Me logueo con un profesor
        res = self.client.post('/api/v1/auth/login/', {'email': self.data_prof1['email'], 'password': self.data_prof1['password']})
        resul = json.loads(res.content)
        self.assertEqual(resul['data']['email'], self.data_prof1['email'])
        # Me logueo con un profesor
        res = self.client.get('/api/v1/auth/permisos/')
        resul = json.loads(res.content)
        self.assertEqual(resul['permissions'][0]['evento'], 'create')