from django.test import TestCase
from gestion_tfg.models import Tfg, Profesor, Alumno
from django.contrib.auth.models import User, Group

from gestion_tfg.servicios import tfg_services

###################   PROPUESTA   ########################
#Usar como username que es unico el email de la ugr

class TfgServicesTests(TestCase):
    def setUp(self):

        self.prof1_username = 'ejemplo@ugr.es'
        self.prof1_nombre = 'profesor 1'
        self.prof1_apellidos = 'apellido 1 apellido 12'
        self.prof1_departamento = 'departamento 1'

        self.prof2_username = 'ejemplo2@ugr.es'
        self.prof2_nombre = 'profesor 2'
        self.prof2_apellidos = 'apellido 2 apellido 22'
        self.prof2_departamento = 'departamento 2'

    def test_insert_profesor_vacio(self):

        profesor = Profesor()
        result = tfg_services.insert_profesor(profesor)
        self.assertEqual(result, False)

    def test_insert_profesor_repetido(self):

        profesor1 = Profesor(username=self.prof1_username, first_name= self.prof1_nombre,
                             last_name= self.prof1_apellidos, departamento=self.prof1_departamento)
        result = tfg_services.insert_profesor(profesor1)
        self.assertEqual(result.username, profesor1.username)
        result = tfg_services.insert_profesor(profesor1)
        self.assertEqual(result, False)

    def test_insert_profesor_error(self):

        self.prof1_username = '34@ugr.es'
        profesor1 = Profesor(username=self.prof1_username, first_name=self.prof1_nombre, last_name=self.prof1_apellidos,
                             departamento=self.prof1_departamento)
        result = tfg_services.insert_profesor(profesor1)
        self.assertEqual(result, False)

        username = 'ejemplo34@ug4r.es'
        profesor1 = Profesor(username=username, first_name= self.prof1_nombre,last_name= self.prof1_apellidos,
                             departamento=self.prof1_departamento)
        result = tfg_services.insert_profesor(profesor1)
        self.assertEqual(result, False)

        username = 'ejemplo34@ugr..es'
        profesor1 = Profesor(username=username, first_name= self.prof1_nombre,last_name= self.prof1_apellidos,
                             departamento=self.prof1_departamento)
        result = tfg_services.insert_profesor(profesor1)
        self.assertEqual(result, False)

        username = 'ejemplo34@ugr.com'
        profesor1 = Profesor(username=username, first_name= self.prof1_nombre,last_name= self.prof1_apellidos,
                             departamento=self.prof1_departamento)
        result = tfg_services.insert_profesor(profesor1)
        self.assertEqual(result, False)

        username = 'ejemplo34@correo.ugr.es'
        profesor1 = Profesor(username=username, first_name= self.prof1_nombre,last_name= self.prof1_apellidos,
                             departamento=self.prof1_departamento)
        result = tfg_services.insert_profesor(profesor1)
        self.assertEqual(result, False)

    def test_insert_profesor_username(self):

        profesor1 = Profesor(first_name=self.prof1_nombre, last_name= self.prof1_apellidos, departamento=self.prof1_departamento)
        result = tfg_services.insert_profesor(profesor1)
        self.assertEqual(result, False)

    def test_insert_profesor_nombre(self):

        profesor1 = Profesor(username=self.prof1_username, last_name= self.prof1_apellidos, departamento=self.prof1_departamento)
        result = tfg_services.insert_profesor(profesor1)
        self.assertEqual(result, False)

    def test_insert_profesor_apellidos(self):

        profesor1 = Profesor(username=self.prof1_username, first_name= self.prof1_nombre, departamento=self.prof1_departamento)
        result = tfg_services.insert_profesor(profesor1)
        self.assertEqual(result, False)

    def test_insert_profesor_departamento(self):

        profesor1 = Profesor(username=self.prof1_username, first_name=self.prof1_nombre, last_name=self.prof1_apellidos)
        result = tfg_services.insert_profesor(profesor1)
        self.assertEqual(result, False)

    def test_insert_profesor_valido(self):

        profesor1 = Profesor(username=self.prof1_username, first_name=self.prof1_nombre, last_name=self.prof1_apellidos,
                             departamento=self.prof1_departamento)
        result = tfg_services.insert_profesor(profesor1)
        self.assertEqual(result.username, profesor1.username)
