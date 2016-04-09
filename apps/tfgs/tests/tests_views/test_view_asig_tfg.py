__author__ = 'tonima'
from django.contrib.auth.models import Group
from django.test import TestCase
import simplejson as json
from rest_framework.test import APIClient

from model.models import Profesor, Tfg, Alumno


class TfgServicesTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.grupo_alumnos = Group.objects.get(name='Alumnos')
        self.grupo_profesores = Group.objects.get(name='Profesores')

        self.user_tutor_tfg = Profesor(username='prof_ejemplo@ugr.es', first_name='profesor 1',
                                       last_name='apellido 1 apellido 12', departamento='el mas mejor')
        self.user_cotutor_tfg = Profesor(username='prof_ejemplo2@ugr.es', first_name='profesor 2',
                                         last_name='apellido 12 apellido 122', departamento='el mas mejor')
        self.user_cotutor_tfg.save()
        self.user_tutor_tfg.save()
        self.grupo_profesores.user_set.add(self.user_cotutor_tfg)
        self.grupo_profesores.user_set.add(self.user_tutor_tfg)

        self.data_alum1 = Alumno(username='ejemplo@correo.ugr.es', first_name='alumno 1',
                                 last_name='apellido 1 apellido 12')
        self.data_alum2 = Alumno(username='ejemplo2@correo.ugr.es', first_name='alumno 2',
                                 last_name='apellido 12 apellido 122')
        self.data_alum2.save()
        self.data_alum1.save()
        self.grupo_alumnos.user_set.add(self.data_alum2)
        self.grupo_alumnos.user_set.add(self.data_alum1)

        self.tfg1 = Tfg(tipo='tipo1', titulo='titulo1', n_alumnos=2,
                        descripcion='descripcion', conocimientos_previos='conocimientos_previos',
                        hard_soft='hard_soft',
                        tutor=self.user_tutor_tfg, cotutor=self.user_cotutor_tfg)
        self.tfg2 = Tfg(tipo='tipo2', titulo='titulo2', n_alumnos=2,
                        descripcion='descripcion2', conocimientos_previos='conocimientos_previos2',
                        hard_soft='hard_soft2',
                        tutor=self.user_tutor_tfg, cotutor=self.user_cotutor_tfg)
        self.tfg2.save()
        self.tfg1.save()

    def test_ws_tfgs_error(self):
        # Asigno el tfg
        res = self.client.post('/asig_tfg/',
                            {'titulo': self.tfg1.titulo,
                                    'username': self.data_alum1.username})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Asignar tfg a alumno con un tfg ya asignado
        res = self.client.post('/asig_tfg/',
                               {'titulo': self.tfg1.titulo,
                                'username': self.data_alum2.username})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], "Tfg ya asignado")

        # Alumno ya con un tfg asignado
        res = self.client.post('/asig_tfg/',
                               {'titulo': self.tfg2.titulo,
                                'username': self.data_alum1.username})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], "Error en los parametros de entrada")

        # Alumno2 ya con un tfg asignado
        res = self.client.post('/asig_tfg/',
                               {'titulo': self.tfg2.titulo,
                                'username': self.data_alum2.username,
                                'username2': self.data_alum1.username})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], "Error en el segundo alumno")

        # TODO Controlar que los alumnos no sean iguales
        # Alumno3 ya con un tfg asignado
        res = self.client.post('/asig_tfg/',
                               {'titulo': self.tfg2.titulo,
                                'username': self.data_alum2.username,
                                'username2': self.data_alum2.username,
                                'username3': self.data_alum1.username})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], False)
        self.assertEqual(resul['message'], "Error en el tercer alumno")

        # Dejo la BD como estaba
        res = self.client.post('/profesores/delete_profesor/',
                     {'username': self.user_tutor_tfg.username})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        res = self.client.post('/profesores/delete_profesor/',
                             {'username': self.user_cotutor_tfg.username})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        res = self.client.post('/alumnos/delete_alumno/',
                     {'username': self.data_alum1.username})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        res = self.client.post('/alumnos/delete_alumno/',
                             {'username': self.data_alum2.username})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
