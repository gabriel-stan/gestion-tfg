# -*- coding: utf-8 -*-
from django.test import TestCase
from rest_framework.test import APIClient
from authentication.models import Usuario
from eventos.models import Tipo_Evento
import simplejson as json


class EventosServicesTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.data_admin = dict(email='admin@admin.es', first_name='admin 1',
                               last_name='apellido 1 apellido 12', password='0000', is_admin=True)
        Usuario.objects.create_superuser(**self.data_admin)

        # tipo_event = Tipo_Evento.objects.create(nombre='Convocatoria', codigo='CONV')

        self.data_evento1 = dict(content=dict(contenido='admin2@admin.es', tipo='CONV_JUN',
                               titulo='titulo 1', desde='01/07/2016', hasta='20/07/2016'))

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
