# -*- coding: utf-8 -*-
from django.test import TestCase
from rest_framework.test import APIClient
from authentication.models import Usuario
from eventos.models import Tipo_Evento
import simplejson as json


class EventosServicesTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.data_admin = dict(email='admin@admin.es', first_name='admin 1', dni='75169053G',
                               last_name='apellido 1 apellido 12', password='0000', is_admin=True)
        Usuario.objects.create_superuser(**self.data_admin)

        self.data_user = dict(email='admin2@admin.es', first_name='admin 1',
                               last_name='apellido 1 apellido 12', password='0000', is_admin=True)
        Usuario.objects.create_user(**self.data_user)

        # tipo_event = Tipo_Evento.objects.create(nombre='Convocatoria', codigo='CONV')

        self.data_evento1 = dict(content=dict(contenido='admin2@admin.es', convocatoria='CONV_JUN', tipo='ASIG_TFG',
                                 titulo='titulo 1', desde='2016-08-04T22:00:00.000Z', hasta='2016-08-14T15:00:00.000Z'))

        self.data_evento2 = dict(content=dict(contenido='admin2@admin.es', convocatoria='INFOR',
                                 titulo='titulo 1'))

    def test_ws_eventos_post(self):
        # Me logueo con un admin
        res = self.client.post('/api/v1/auth/login/', {'email': self.data_admin['email'],
                                                       'password': self.data_admin['password']})
        resul = json.loads(res.content)
        self.assertEqual(resul['data']['email'], self.data_admin['email'])
        # Inserto un evento
        res = self.client.post('/api/v1/events/',  self.data_evento1, format='json')
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        self.assertEqual(resul['data']['contenido'], self.data_evento1['content']['contenido'])

        # Inserto un evento informativo
        res = self.client.post('/api/v1/events/',  self.data_evento2, format='json')
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        self.assertEqual(resul['data']['contenido'], self.data_evento2['content']['contenido'])

        # Me logueo aon otro usuario
        res = self.client.post('/api/v1/auth/login/', {'email': self.data_user['email'],
                                                       'password': self.data_user['password']})
        resul = json.loads(res.content)
        self.assertEqual(resul['data']['email'], self.data_user['email'])

        # Obtengo los eventos
        res = self.client.get('/api/v1/events/')
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        self.assertEqual(resul['data'][0]['autor']['dni'], None)

    def test_ws_convocatoria_eventos_post(self):
        # Me logueo con un admin
        res = self.client.post('/api/v1/auth/login/', {'email': self.data_admin['email'],
                                                       'password': self.data_admin['password']})
        resul = json.loads(res.content)
        self.assertEqual(resul['data']['email'], self.data_admin['email'])
        # Obtengo los tipos de eventos
        res = self.client.get('/api/v1/convocatorias/')
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        self.assertEqual(resul['data'][0]['codigo'], 'CONV_JUN')

    def test_ws_tipos_eventos_post(self):
        # Me logueo con un admin
        res = self.client.post('/api/v1/auth/login/', {'email': self.data_admin['email'],
                                                       'password': self.data_admin['password']})
        resul = json.loads(res.content)
        self.assertEqual(resul['data']['email'], self.data_admin['email'])
        # Obtengo los tipos de eventos
        res = self.client.get('/api/v1/tipo_eventos/')
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        self.assertEqual(len(resul['data']), 7)
