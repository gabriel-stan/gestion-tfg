from django.test import TestCase

from old.controller.servicios import tfg_services
from model.models import Alumno


class TfgServicesTests(TestCase):
    def setUp(self):

        self.alumn1_username = 'ejemplo@correo.ugr.es'
        self.alumn1_nombre = 'alumno 1'
        self.alumn1_apellidos = 'apellido 1 apellido 12'

        self.otro_username = 'ejemplo2@correo.ugr.es'
        self.otro_nombre = 'alumno 2'
        self.otro_apellidos = 'apellido 2 apellido 22'

        self.alumno1 = tfg_services.insert_alumno(Alumno(username=self.alumn1_username, first_name=self.alumn1_nombre,
                                                         last_name=self.alumn1_apellidos, password='75169052'))

    def test_delete_alumno_no_existe(self):

        alumno = Alumno(username=self.otro_username, first_name=self.otro_nombre, last_name=self.otro_apellidos)
        result = tfg_services.delete_alumno(alumno)
        self.assertEqual(result['status'], False)

    def test_delete_alumno_existe(self):

        alumno = Alumno.objects.get(username=self.alumn1_username)
        result = tfg_services.delete_alumno(alumno)
        self.assertEqual(result['status'], True)
