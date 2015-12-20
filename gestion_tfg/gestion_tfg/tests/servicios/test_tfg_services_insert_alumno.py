from django.test import TestCase
from gestion_tfg.models import Tfg, Profesor, Alumno
from django.contrib.auth.models import User, Group

from gestion_tfg.servicios import tfg_services

###################   PROPUESTA   ########################
#Usar como username que es unico el email de la ugr

class TfgServicesTests(TestCase):
    def setUp(self):

        self.alumn1_username = 'ejemplo@correo.ugr.es'
        self.alumn1_nombre = 'alumno 1'
        self.alumn1_apellidos = 'apellido 1 apellido 12'

        self.alumn2_username = 'ejemplo2@coreo.ugr.es'
        self.alumn2_nombre = 'alumno 2'
        self.alumn2_apellidos = 'apellido 2 apellido 22'


    def test_user_vacio(self):

        alumno = Alumno()
        result = tfg_services.insert_alumno(alumno)
        self.assertEqual(result, False)

    def test_no_username(self):

        alumno1 = Alumno(first_name=self.alumn1_nombre,last_name= self.alumn1_apellidos)
        result = tfg_services.insert_alumno(alumno1)
        self.assertEqual(result, False)

    def test_user_repetido(self):

        alumno1 = Alumno(username=self.alumn1_username, first_name= self.alumn1_nombre,last_name= self.alumn1_apellidos)
        alumno2 = Alumno(username=self.alumn2_username, first_name= self.alumn2_nombre,last_name= self.alumn2_apellidos)
        result = tfg_services.insert_alumno(alumno1)
        self.assertEqual(result.username, alumno1.username)
        result = tfg_services.insert_alumno(alumno2)
        self.assertEqual(result, False)

    def test_user_error(self):

        self.alumn1_username = '34@correo.ugr.es'
        alumno1 = Alumno(username=self.alumn1_username, first_name= self.alumn1_nombre,last_name= self.alumn1_apellidos)
        result = tfg_services.insert_alumno(alumno1)
        self.assertEqual(result, False)

    def test_user_no_nombre(self):

        alumno1 = Alumno(username=self.alumn1_username, first_name= self.alumn1_nombre)
        result = tfg_services.insert_alumno(alumno1)
        self.assertEqual(result, False)

    def test_user_no_apellidos(self):

        alumno1 = Alumno(username=self.alumn1_username, first_name= self.alumn1_nombre)
        result = tfg_services.insert_alumno(alumno1)
        self.assertEqual(result, False)

    def test_user_valido(self):

        alumno1 = Alumno(username=self.alumn1_username, first_name=self.alumn1_nombre, last_name=self.alumn1_apellidos)
        result = tfg_services.insert_alumno(alumno1)
        self.assertEqual(result.username, alumno1.username)
