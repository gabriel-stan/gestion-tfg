from django.test import TestCase
from authentication.models import Alumno
from authentication.serializers import AlumnoSerializer


###################   PROPUESTA   ########################
#Usar como username que es unico el email de la ugr

class TfgServicesTests(TestCase):
    def setUp(self):

        self.alumn1_username = 'ejemplo@correo.ugr.es'
        self.alumn1_nombre = 'alumno 1'
        self.alumn1_apellidos = 'apellido 1 apellido 12'

        self.alumn2_username = 'ejemplo2@correo.ugr.es'
        self.alumn2_nombre = 'alumno 2'
        self.alumn2_apellidos = 'apellido 2 apellido 22'
        self.serializer_class = AlumnoSerializer

    def test_insert_alumno(self):

        alumno = self.serializer_class()
        result = alumno.create({'email': self.alumn1_username, 'first_name': self.alumn1_nombre,
                                'last_name': self.alumn1_apellidos})
        self.assertEqual(result['data'].email, self.alumn1_username)

        result = alumno.create({'email': self.alumn1_username, 'first_name': self.alumn1_nombre,
                                'last_name': self.alumn1_apellidos})
        self.assertEqual(result['status'], False)

    def test_insert_alumno_error(self):

        alumno = self.serializer_class()
        result = alumno.create({'email': '34@correo.ugr.es', 'first_name': self.alumn1_nombre,
                                'last_name': self.alumn1_apellidos})
        self.assertEqual(result['status'], False)

        alumno = self.serializer_class()
        result = alumno.create({'email': 'ejemplo34@coreo.ugr.es', 'first_name': self.alumn1_nombre,
                                'last_name': self.alumn1_apellidos})
        self.assertEqual(result['status'], False)

        alumno = self.serializer_class()
        result = alumno.create({'email': 'ejemplo34@correo..ugr.es', 'first_name': self.alumn1_nombre,
                                'last_name': self.alumn1_apellidos})
        self.assertEqual(result['status'], False)

        alumno = self.serializer_class()
        result = alumno.create({'email': 'ejemplo34@correo.ugr.com', 'first_name': self.alumn1_nombre,
                                'last_name': self.alumn1_apellidos})
        self.assertEqual(result['status'], False)

        alumno = self.serializer_class()
        result = alumno.create({'email': 'ejemplo34@ugr.es', 'first_name': self.alumn1_nombre,
                                'last_name': self.alumn1_apellidos})
        self.assertEqual(result['status'], False)

    def test_insert_alumno_nombre(self):

        alumno = self.serializer_class()
        result = alumno.create({'email': self.alumn1_username, 'last_name': self.alumn1_apellidos})
        self.assertEqual(result['status'], True)

    def test_insert_alumno_apellidos(self):

        alumno = self.serializer_class()
        result = alumno.create({'email': self.alumn1_username, 'firs_name': self.alumn1_nombre})
        self.assertEqual(result['status'], True)
