__author__ = 'tonima'
from django.test import TestCase
from rest_framework.test import APIClient
from authentication.models import Usuario, Departamento
from tfgs.models import Titulacion
import simplejson as json


class TfgServicesTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.data_admin = dict(email='admin@admin.es', first_name='admin 1',
                               last_name='apellido 1 apellido 12', password='0000', is_admin=True)
        Usuario.objects.create_superuser(**self.data_admin)

        dep = Departamento.objects.create(nombre='departamento1', codigo='AAA')

        titulacion = Titulacion.objects.create(nombre='Ingenieria Informatica', codigo='IF')

        self.data_prof1 = dict(email='prof_ejemplo@ugr.es', first_name='profesor 1',
                               last_name='apellido 1 apellido 12', departamento=dep.codigo, password='75169052')

        self.data_prof2 = dict(email='prof_ejemplo2@ugr.es', first_name='profesor 2',
                               last_name='apellido 12 apellido 122', departamento=dep.codigo, password='75169052')

        self.data_tfg1 = dict(tipo='tipo1', titulo='titulo1',
                              n_alumnos=2, descripcion='descripcion',
                              conocimientos_previos='conocimientos previos',
                              hard_soft='hard_soft', tutor=self.data_prof1['email'],
                              cotutor=self.data_prof2['email'], titulacion=titulacion.codigo)

        self.data_tfg2 = dict(tipo='tipo1', titulo='titulo1',
                              n_alumnos=2, descripcion='descripcion',
                              conocimientos_previos='conocimientos previos',
                              hard_soft='hard_soft', tutor=self.data_prof2['email'],
                              cotutor=self.data_prof2['email'], titulacion=titulacion.codigo)

        self.data_tfg_error = dict(titulo='titulo1',
                                   n_alumnos=2, descripcion='descripcion',
                                   conocimientos_previos='conocimientos previos',
                                   hard_soft='conocimientos previos', tutor='prof_ejemplo@ugr.es',
                                   cotutor='prof_ejemplo2@ugr.es', titulacion=titulacion.codigo)

        self.data_alum1 = dict(email='alumno1@correo.ugr.es', first_name='profesor 2',
                               last_name='apellido 12 apellido 122', password='75169052')

    def test_ws_tfgs(self):
        # Login como administrador
        res = self.client.post('/api/v1/auth/login/', dict(email=self.data_admin['email'],
                                                           password=self.data_admin['password']))
        resul = json.loads(res.content)
        self.assertEqual(resul['data']['email'], self.data_admin['email'])

        # Inserto un profesor y un alumno
        res = self.client.post('/api/v1/profesores/', self.data_prof1)
        resul = json.loads(res.content)
        self.assertEqual(resul['data']['email'], self.data_prof1['email'])

        res = self.client.post('/api/v1/alumnos/', self.data_alum1)
        resul = json.loads(res.content)
        self.assertEqual(resul['data']['email'], self.data_alum1['email'])

        # Intento obtener todos ls TFGs, pero no hay ninguno
        res = self.client.get('/api/v1/tfgs/')
        resul = json.loads(res.content)
        self.assertEqual(resul['message'], 'No hay tfgs almacenados')

        # El tfg no existe
        res = self.client.get('/api/v1/tfgs/', {'titulo': self.data_tfg1['titulo']})
        resul = json.loads(res.content)
        self.assertEqual(resul['message'], 'El tfg indicado no existe')

        # inserto un tfg erroneo, sin tipo
        res = self.client.post('/api/v1/tfgs/', self.data_tfg_error)
        resul = json.loads(res.content)
        self.assertEqual(resul['message'], 'Tipo de TFG necesario')

        # inserto un tfg incorrecto, el cotutor no existe
        res = self.client.post('/api/v1/tfgs/', self.data_tfg1)
        resul = json.loads(res.content)
        self.assertEqual(resul['message'], 'El cotutor no existe')

        #Inserto el cotutor
        res = self.client.post('/api/v1/profesores/', self.data_prof2)
        resul = json.loads(res.content)
        self.assertEqual(resul['data']['email'], self.data_prof2['email'])

        # inserto un tfg correcto
        res = self.client.post('/api/v1/tfgs/', self.data_tfg1)
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # El tfg existe
        res = self.client.get('/api/v1/tfgs/', {'titulo': self.data_tfg1['titulo']})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Asigno el TFG
        res = self.client.post('/api/v1/tfgs_asig/', {'tfg': self.data_tfg1['titulo'], 'alumno1': self.data_alum1['email']})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Le asigno una convocatoria
        res = self.client.put('/api/v1/tfgs_asig/', {'tfg': self.data_tfg1['titulo'], 'convocatoria': 0})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
