from django.test import TestCase
from serializers import AlumnoSerializer
from controller.servicios import tfg_services
from model.models import Alumno


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

    def test_insert_alumno_vacio(self):

        alumno = AlumnoSerializer()
        result = alumno.create({'email': self.alumn1_username, 'first_name': self.alumn1_nombre,
                                'last_name': self.alumn1_apellidos})
        self.assertEqual(result.email, self.alumn1_username)

    def test_insert_alumno_repetido(self):

        alumno1 = Alumno(username=self.alumn1_username, first_name=self.alumn1_nombre, last_name=self.alumn1_apellidos)
        result = tfg_services.insert_alumno(alumno1)
        self.assertEqual(result['data'].username, alumno1.username)
        result = tfg_services.insert_alumno(alumno1)
        self.assertEqual(result['status'], False)

    def test_insert_alumno_error(self):

        username = '34@correo.ugr.es'
        alumno1 = Alumno(username=username, first_name= self.alumn1_nombre,last_name= self.alumn1_apellidos)
        result = tfg_services.insert_alumno(alumno1)
        self.assertEqual(result['status'], False)

        username = 'ejemplo34@coreo.ugr.es'
        alumno1 = Alumno(username=username, first_name= self.alumn1_nombre,last_name= self.alumn1_apellidos)
        result = tfg_services.insert_alumno(alumno1)
        self.assertEqual(result['status'], False)

        username = 'ejemplo34@correo..ugr.es'
        alumno1 = Alumno(username=username, first_name= self.alumn1_nombre,last_name= self.alumn1_apellidos)
        result = tfg_services.insert_alumno(alumno1)
        self.assertEqual(result['status'], False)

        username = 'ejemplo34@correo.ugr.com'
        alumno1 = Alumno(username=username, first_name= self.alumn1_nombre,last_name= self.alumn1_apellidos)
        result = tfg_services.insert_alumno(alumno1)
        self.assertEqual(result['status'], False)

        username = 'ejemplo34@ugr.es'
        alumno1 = Alumno(username=username, first_name= self.alumn1_nombre,last_name= self.alumn1_apellidos)
        result = tfg_services.insert_alumno(alumno1)
        self.assertEqual(result['status'], False)

    def test_insert_alumno_username(self):

        alumno1 = Alumno(first_name=self.alumn1_nombre,last_name= self.alumn1_apellidos)
        result = tfg_services.insert_alumno(alumno1)
        self.assertEqual(result['status'], False)

    def test_insert_alumno_nombre(self):

        alumno1 = Alumno(username=self.alumn1_username, last_name= self.alumn1_apellidos)
        result = tfg_services.insert_alumno(alumno1)
        self.assertEqual(result['status'], False)

    def test_insert_alumno_apellidos(self):

        alumno1 = Alumno(username=self.alumn1_username, first_name= self.alumn1_nombre)
        result = tfg_services.insert_alumno(alumno1)
        self.assertEqual(result['status'], False)

    def test_insert_alumno_valido(self):

        alumno1 = Alumno(username=self.alumn1_username, first_name=self.alumn1_nombre, last_name=self.alumn1_apellidos)
        result = tfg_services.insert_alumno(alumno1)
        self.assertEqual(result['data'].username, alumno1.username)
