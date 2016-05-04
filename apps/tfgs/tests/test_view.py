__author__ = 'tonima'
from django.test import TestCase
from rest_framework.test import APIClient
import simplejson as json


class TfgServicesTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.data_prof1 = dict(email='prof_ejemplo@ugr.es', first_name='profesor 1',
                               last_name='apellido 1 apellido 12', departamento='el mas mejor', password='75169052')

        self.data_prof2 = dict(email='prof_ejemplo2@ugr.es', first_name='profesor 2',
                               last_name='apellido 12 apellido 122', departamento='el mas mejor', password='75169052')

        self.data_tfg1 = dict(tipo='tipo1', titulo='titulo1',
                              n_alumnos=2, descripcion='descripcion',
                              conocimientos_previos='conocimientos previos',
                              hard_soft='hard_soft', tutor=self.data_prof1['email'],
                              cotutor=self.data_prof2['email'])

        self.data_tfg2 = dict(tipo='tipo1', titulo='titulo1',
                              n_alumnos=2, descripcion='descripcion',
                              conocimientos_previos='conocimientos previos',
                              hard_soft='hard_soft', tutor=self.data_prof2['email'],
                              cotutor=self.data_prof2['email'])

        self.data_tfg_error = dict(titulo='titulo1',
                                   n_alumnos=2, descripcion='descripcion',
                                   conocimientos_previos='conocimientos previos',
                                   hard_soft='conocimientos previos', tutor='prof_ejemplo@ugr.es',
                                   cotutor='prof_ejemplo2@ugr.es')
        self.data_alum1 = dict(email='alumno1@correo.ugr.es', first_name='profesor 2',
                               last_name='apellido 12 apellido 122', password='75169052')

    def test_ws_tfgs_error(self):
        # Sin tfgs
        res = self.client.post('/api/v1/profesores/', self.data_prof1)
        resul = json.loads(res.content)
        self.assertEqual(resul['data']['email'], self.data_prof1['email'])
        res = self.client.post('/api/v1/auth/login/', dict(email=self.data_prof1['email'],
                                                           password=self.data_prof1['password']))
        res = self.client.post('/api/v1/alumnos/', self.data_alum1)
        resul = json.loads(res.content)

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
        self.assertEqual(resul['message']['tipo'][0], 'This field is required.')

        # inserto un tfg erroneo, sin titulo
        res = self.client.post('/api/v1/tfgs/', self.data_tfg1)
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Borrar tfg que no existe
        res = self.client.post('/api/v1/tfgs_asig/', {'tfg': self.data_tfg1['titulo'], 'alumno1': self.data_alum1['email']})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
    #
    #     # Modificar un tfg que no existe
    #     res = self.client.post('/tfgs/update_tfg/',
    #                            {'titulo': self.data_tfg1['titulo'], 'campos': json.dumps({'tipo': 'tipo 2'})})
    #     resul = json.loads(res.content)
    #     self.assertEqual(resul['status'], False)
    #     self.assertEqual(resul['message'], "El tfg indicado no existe")
    #
    #     # Dejo la BD como estaba
    #     res = self.client.post('/profesores/delete_profesor/',
    #                            {'username': self.data_prof1['username']})
    #     resul = json.loads(res.content)
    #     self.assertEqual(resul['status'], True)
    #     res = self.client.post('/profesores/delete_profesor/',
    #                            {'username': self.data_prof2['username']})
    #     resul = json.loads(res.content)
    #     self.assertEqual(resul['status'], True)
    #
    # def test_ws_tfgs(self):
    #     # inserto un tfg
    #     res = self.client.post('/tfgs/', self.data_tfg1)
    #     resul = json.loads(res.content)
    #     self.assertEqual(resul['status'], True)
    #
    #     # tfg recien insertado
    #     res = self.client.get('/tfgs/', {'titulo': self.data_tfg1['titulo']})
    #     resul = json.loads(res.content)
    #     self.assertEqual(resul['status'], True)
    #     self.assertEqual(resul['data']['titulo'], self.data_tfg1['titulo'])
    #
    #     # Todos los tfgs
    #     res = self.client.get('/tfgs/')
    #     resul = json.loads(res.content)
    #     self.assertEqual(resul['status'], True)
    #     self.assertEqual(resul['data'][0]['titulo'], self.data_tfg1['titulo'])
    #
    #     # Modificar un tfg con parametros  incorrectos
    #     res = self.client.post('/tfgs/update_tfg/',
    #                            {'tfg': 'ejemplo@correo.ugr.es',
    #                             'nocampos': json.dumps({'titulo': 'otro tfg 2'})})
    #     resul = json.loads(res.content)
    #     self.assertEqual(resul['status'], False)
    #     self.assertEqual(resul['message'], "Error en la llamada")
    #
    #     # Modificar un tfg
    #     res = self.client.post('/tfgs/update_tfg/',
    #                            {'titulo': self.data_tfg1['titulo'],
    #                             'campos': json.dumps({'titulo': 'otro tfg 1'})})
    #     resul = json.loads(res.content)
    #     self.assertEqual(resul['status'], True)
    #
    #     # Dejo la BD como estaba
    #     res = self.client.post('/tfgs/delete_tfg/',
    #                            {'titulo': 'otro tfg 1'})
    #     resul = json.loads(res.content)
    #     self.assertEqual(resul['status'], True)
    #
    #     res = self.client.post('/profesores/delete_profesor/',
    #                            {'username': self.data_prof1['username']})
    #     resul = json.loads(res.content)
    #     self.assertEqual(resul['status'], True)
    #     res = self.client.post('/profesores/delete_profesor/',
    #                            {'username': self.data_prof2['username']})
    #     resul = json.loads(res.content)
    #     self.assertEqual(resul['status'], True)
