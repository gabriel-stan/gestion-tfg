__author__ = 'tonima'
from django.test import TestCase
import simplejson as json
from rest_framework.test import APIClient


class TfgServicesTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # self.data_login = Profesor(username='ejemplo3@ugr.es', first_name='profesor 1',
        #                        last_name='apellido 1 apellido 12', departamento='el mas mejor', password='75169052')
        # grupo_profesores = Group.objects.get(name='Profesores')
        # self.data_login.save()
        # grupo_profesores.user_set.add(self.data_login)

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
        self.assertEqual(resul['message'], 'No tienes los permisos necesarios')

    #
    #     # El alumno no existe
    #     res = self.client.get('/alumnos/',  {'username': 'pepito'})
    #     resul = json.loads(res.content)
    #     self.assertEqual(resul['status'], False)
    #     self.assertEqual(resul['message'], 'El alumno indicado no existe')
    #
    #     # inserto un alumno erroneo
    #     res = self.client.post('/alumnos/', self.data_alum_error)
    #     resul = json.loads(res.content)
    #     self.assertEqual(resul['status'], False)
    #     self.assertEqual(resul['message'], 'El correo no es correcto')
    #
    #     # Borrar alumno que no existe
    #     res = self.client.post('/alumnos/delete_alumno/',
    #                          {'username': 'pepito'})
    #     resul = json.loads(res.content)
    #     self.assertEqual(resul['status'], False)
    #     self.assertEqual(resul['message'], "El alumno indicado no existe")
    #
    #     # Modificar un alumno que no existe
    #     res = self.client.post('/alumnos/update_alumno/',
    #                          {'alumno': 'pepito', 'campos': json.dumps({'first_name': 'otro alumno 2'})})
    #     resul = json.loads(res.content)
    #     self.assertEqual(resul['status'], False)
    #     self.assertEqual(resul['message'], "El alumno indicado no existe")
    #
    def test_ws_alumnos_post(self):
        # inserto un alumno
        res = self.client.post('/api/v1/alumnos/', self.data_alum1)
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Modificar un alumno
        res = self.client.put('/api/v1/alumnos/', {'alumno': self.data_alum1['email'], 'datos': json.dumps({'first_name': 'otro alumno 2'})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
    #
    #     # Alumno recien insertado
    #     res = self.client.get('/alumnos/',  {'username': 'ejemplo@correo.ugr.es'})
    #     resul = json.loads(res.content)
    #     self.assertEqual(resul['status'], True)
    #     self.assertEqual(resul['data']['first_name'], 'alumno 1')
    #
    #     # Todos los alumnos
    #     res = self.client.get('/alumnos/')
    #     resul = json.loads(res.content)
    #     self.assertEqual(resul['status'], True)
    #     self.assertEqual(resul['data'][0]['first_name'], 'alumno 1')
    #
    #     resul = json.loads(res.content)
    #     self.assertEqual(resul['status'], False)
    #     self.assertEqual(resul['message'], "Error en la llamada")
    #
    #     # Modificar un alumno
    #     res = self.client.post('/alumnos/update_alumno/',
    #                         {'alumno': self.data_alum1['username'],
    #                               'campos': json.dumps({'first_name': 'otro alumno 1'})})
    #     resul = json.loads(res.content)
    #     self.assertEqual(resul['status'], True)
    #
    #     # Dejo la BD como estaba
    #     res = self.client.post('/alumnos/delete_alumno/',
    #                          {'username': 'ejemplo@correo.ugr.es'})
    #     resul = json.loads(res.content)
    #     self.assertEqual(resul['status'], True)

    def test_ws_profesores_get(self):
        # inserto un profesor
        res = self.client.post('/api/v1/profesores/', self.data_prof1)
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Modificar un profesor
        res = self.client.put('/api/v1/profesores/', {'profesor': self.data_prof1['email'], 'datos': json.dumps({'first_name': 'otro profesor 2'})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Me logueo con un profesor
        res = self.client.post('/api/v1/auth/login/', {'email': self.data_prof1['email'], 'password': self.data_prof1['password']})
        resul = json.loads(res.content)
        self.assertEqual(resul['email'], self.data_prof1['email'])
        # Introduzco 2 alumnos
        res = self.client.post('/api/v1/alumnos/', self.data_alum1)
        res = self.client.post('/api/v1/alumnos/', self.data_alum2)
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        # obtengo todos los alumnos por que soy un profesor
        res = self.client.get('/api/v1/alumnos/')
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
