__author__ = 'tonima'
from django.contrib.auth.models import Group
from django.test import TestCase
from model.models import Profesor
from controller.servicios import tfg_services
import simplejson as json
from rest_framework.test import APIClient

class TfgServicesTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.data_prof1 = dict(username='prof_ejemplo@ugr.es', first_name='profesor 1',
                               last_name='apellido 1 apellido 12', departamento='el mas mejor')

        self.data_prof2 = dict(username='prof_ejemplo2@ugr.es', first_name='profesor 2',
                               last_name='apellido 12 apellido 122', departamento='el mas mejor')

        self.user_tutor_tfg = self.client.post('http://127.0.0.1:8000/profesores/', data=self.data_prof1)
        self.user_cotutor_tfg = self.client.post('http://127.0.0.1:8000/profesores/', data=self.data_prof2)

        self.data_alum1 = dict(username='ejemplo@correo.ugr.es', first_name='alumno 1',
                               last_name='apellido 1 apellido 12')

        self.data_alum2 = dict(username='ejemplo2@correo.ugr.es', first_name='alumno 2',
                               last_name='apellido 12 apellido 122')

        self.user_alum1_tfg = self.client.post('http://127.0.0.1:8000/alumnos/', data=self.data_alum1)
        self.user_alum2_tfg = self.client.post('http://127.0.0.1:8000/alumnos/', data=self.data_alum2)

        self.data_tfg1 = dict(tipo='tipo1', titulo='titulo1',
                   n_alumnos=2, descripcion='descripcion',
                   conocimientos_previos='conocimientos previos',
                   hard_soft='hard_soft', tutor=self.data_prof1['username'],
                   cotutor=self.data_prof2['username'])

        self.data_tfg2 = dict(tipo='tipo2', titulo='titulo2',
                   n_alumnos=2, descripcion='descripcion2',
                   conocimientos_previos='conocimientos previos2',
                   hard_soft='hard_soft2', tutor=self.data_prof2['username'],
                   cotutor=self.data_prof2['username'])

        self.data_tfg_error = dict(titulo='titulo1',
                   n_alumnos=2, descripcion='descripcion',
                   conocimientos_previos='conocimientos previos',
                   hard_soft='conocimientos previos', tutor=self.user_tutor_tfg,
                   cotutor=self.user_cotutor_tfg)

        self.tfg1 = self.client.post('http://127.0.0.1:8000/tfgs/', data=self.data_tfg1)
        self.tfg2 = self.client.post('http://127.0.0.1:8000/tfgs/', data=self.data_tfg2)

    def test_ws_tfgs_error(self):
        # Asigno el tfg
        res = self.client.post('http://127.0.0.1:8000/asig_tfg/',
                            {'titulo': self.data_tfg1['titulo'],
                                    'username': self.data_alum1['username']})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Asignar tfg a alumno con un tfg ya asignado
        res = self.client.post('http://127.0.0.1:8000/asig_tfg/',
                               {'titulo': self.data_tfg1['titulo'],
                                'username': self.data_alum2['username']})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], "Tfg ya asignado")

        # Alumno ya con un tfg asignado
        res = self.client.post('http://127.0.0.1:8000/asig_tfg/',
                               {'titulo': self.data_tfg2['titulo'],
                                'username': self.data_alum1['username']})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], "Error en los parametros de entrada")

        # Alumno2 ya con un tfg asignado
        res = self.client.post('http://127.0.0.1:8000/asig_tfg/',
                               {'titulo': self.data_tfg2['titulo'],
                                'username': self.data_alum2['username'],
                                'username2': self.data_alum1['username']})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], "Error en el segundo alumno")

        # TODO Controlar que los alumnos no sean iguales
        # Alumno3 ya con un tfg asignado
        res = self.client.post('http://127.0.0.1:8000/asig_tfg/',
                               {'titulo': self.data_tfg2['titulo'],
                                'username': self.data_alum2['username'],
                                'username2': self.data_alum2['username'],
                                'username3': self.data_alum1['username']})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], "Error en el tercer alumno")

        # Dejo la BD como estaba
        res = self.client.post('http://127.0.0.1:8000/profesores/delete_profesor/',
                     {'username': self.data_prof1['username']})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        res = self.client.post('http://127.0.0.1:8000/profesores/delete_profesor/',
                             {'username': self.data_prof2['username']})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        res = self.client.post('http://127.0.0.1:8000/alumnos/delete_alumno/',
                     {'username': self.data_alum1['username']})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        res = self.client.post('http://127.0.0.1:8000/alumnos/delete_alumno/',
                             {'username': self.data_alum2['username']})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
