from django.test import TestCase
from gestion_tfg.models import Tfg, Alumno
from django.contrib.auth.models import User, Group

from gestion_tfg.servicios import tfg_services


class TfgServicesTests(TestCase):
    def setUp(self):

        self.alumn1_username = 'ejemplo@correo.ugr.es'
        self.alumn1_nombre = 'alumno 1'
        self.alumn1_apellidos = 'apellido 1 apellido 12'

        self.alumno1 = tfg_services.insert_alumno(Alumno(username=self.alumn1_username, first_name=self.alumn1_nombre,
                                                         last_name=self.alumn1_apellidos))


    def test_delete_alumno_existe(self):

        alumno = Alumno.objects.get(username=self.alumn1_username)
        result = tfg_services.delete_alumno(alumno)
        self.assertEqual(result, True)
