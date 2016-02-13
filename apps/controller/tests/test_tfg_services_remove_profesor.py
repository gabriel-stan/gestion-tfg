from django.test import TestCase

from apps.controller.servicios import tfg_services
from apps.model.models import Alumno, Profesor


class TfgServicesTests(TestCase):
    def setUp(self):

        self.prof1_username = 'ejemplo@ugr.es'
        self.prof1_nombre = 'alumno 1'
        self.prof1_apellidos = 'apellido 1 apellido 12'
        self.prof1_departamento = 'departamento 1'

        self.otro_username = 'ejemplo2@ugr.es'
        self.otro_nombre = 'profesor 2'
        self.otro_apellidos = 'apellido 2 apellido 22'
        self.otro_departamento = 'otro departamento'

        self.prof1 = tfg_services.insert_profesor(Profesor(username=self.prof1_username, first_name=self.prof1_nombre,
                                                           last_name=self.prof1_apellidos,
                                                           departamento=self.prof1_departamento))

    def test_delete_alumno_no_existe(self):

        otro_profesor = Profesor(username=self.otro_username, first_name=self.otro_nombre,
                                                         last_name=self.otro_apellidos,
                                                         departamento=self.otro_departamento)
        result = tfg_services.delete_profesor(otro_profesor)
        self.assertEqual(result['status'], False)

    def test_delete_alumno_existe(self):

        profesor = Alumno.objects.get(username=self.prof1_username)
        result = tfg_services.delete_profesor(profesor)
        self.assertEqual(result['status'], True)
