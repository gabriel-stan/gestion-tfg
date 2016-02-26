__author__ = 'tonima'
from django.contrib.auth.models import Group
from django.test import TestCase
from model.models import Profesor
from controller.servicios import tfg_services
import requests
import simplejson as json


class TfgServicesTests(TestCase):
    def setUp(self):

        self.data_prof1 = dict(username='prof_ejemplo@ugr.es', first_name='profesor 1',
                               last_name='apellido 1 apellido 12', departamento='el mas mejor')

        self.data_prof2 = dict(username='prof_ejemplo2@ugr.es', first_name='profesor 2',
                               last_name='apellido 12 apellido 122', departamento='el mas mejor')

        self.user_tutor_tfg = requests.post('http://127.0.0.1:8000/profesores/', data=self.data_prof1)
        self.user_cotutor_tfg = requests.post('http://127.0.0.1:8000/profesores/', data=self.data_prof2)


        self.data_tfg1 = dict(tipo='tipo1', titulo='titulo1',
                   n_alumnos=2, descripcion='descripcion',
                   conocimientos_previos='conocimientos previos',
                   hard_soft='hard_soft', tutor=self.data_prof1['username'],
                   cotutor=self.data_prof2['username'])

        self.data_tfg2 = dict(tipo='tipo1', titulo='titulo1',
                   n_alumnos=2, descripcion='descripcion',
                   conocimientos_previos='conocimientos previos',
                   hard_soft='hard_soft', tutor=self.data_prof2['username'],
                   cotutor=self.data_prof2['username'])

        self.data_tfg_error = dict(titulo='titulo1',
                   n_alumnos=2, descripcion='descripcion',
                   conocimientos_previos='conocimientos previos',
                   hard_soft='conocimientos previos', tutor=self.user_tutor_tfg,
                   cotutor=self.user_cotutor_tfg)

    def test_ws_tfgs_error(self):
        # Sin tfgs
        res = requests.get('http://127.0.0.1:8000/tfgs')
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], 'No hay tfgs almacenados')

        # El tfg no existe
        res = requests.get('http://127.0.0.1:8000/tfgs', params={'titulo': self.data_tfg1['titulo']})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], 'El tfg indicado no existe')

        # inserto un tfg con parametros incorrectos
        res = requests.post('http://127.0.0.1:8000/tfgs/', data='perico')
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], 'Error en la llamada')

        # inserto un tfg erroneo, sin titulo
        res = requests.post('http://127.0.0.1:8000/tfgs/', data=self.data_tfg_error)
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], 'Error en la llamada')

        # Borrar tfg que no existe
        res = requests.post('http://127.0.0.1:8000/tfgs/delete_tfg/',
                            params={'titulo': self.data_tfg1['titulo']})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], "El tfg indicado no existe")

        # Modificar un tfg que no existe
        res = requests.post('http://127.0.0.1:8000/tfgs/update_tfg/',
                            params={'titulo': self.data_tfg1['titulo'], 'campos': json.dumps({'tipo': 'tipo 2'})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], "El tfg indicado no existe")

        res = requests.post('http://127.0.0.1:8000/profesores/delete_profesor/',
                    params={'username': self.data_prof1['username']})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        res = requests.post('http://127.0.0.1:8000/profesores/delete_profesor/',
                            params={'username': self.data_prof2['username']})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

    def test_ws_tfgs(self):
        # inserto un tfg
        res = requests.post('http://127.0.0.1:8000/tfgs/', data=self.data_tfg1)
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # tfg recien insertado
        res = requests.get('http://127.0.0.1:8000/tfgs', params={'titulo': self.data_tfg1['titulo']})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        self.assertEqual(resul['data']['titulo'], self.data_tfg1['titulo'])

        # Todos los tfgs
        res = requests.get('http://127.0.0.1:8000/tfgs')
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        self.assertEqual(resul['data'][0]['titulo'], self.data_tfg1['titulo'])

        # Modificar un tfg con parametros  incorrectos
        res = requests.post('http://127.0.0.1:8000/tfgs/update_tfg/',
                            params={'tfg': 'ejemplo@correo.ugr.es',
                                    'nocampos': json.dumps({'titulo': 'otro tfg 2'})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], "Error en la llamada")

        # Modificar un tfg
        res = requests.post('http://127.0.0.1:8000/tfgs/update_tfg/',
                            data={'titulo': self.data_tfg1['titulo'],
                                  'campos': json.dumps({'titulo': 'otro tfg 1'})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Dejo la BD como estaba
        res = requests.post('http://127.0.0.1:8000/tfgs/delete_tfg/',
                            params={'titulo': 'otro tfg 1'})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        res = requests.post('http://127.0.0.1:8000/profesores/delete_profesor/',
                            params={'username': self.data_prof1['username']})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        res = requests.post('http://127.0.0.1:8000/profesores/delete_profesor/',
                            params={'username': self.data_prof2['username']})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

