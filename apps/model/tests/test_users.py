from apps.model.models import Alumno, Profesor
from django.test import TestCase

nuevo_alumno = {}
nuevo_alumno['username'] = 'nuevo_alumno@correo.ugr.es'
nuevo_alumno['first_name'] = 'apellido2 1'
nuevo_alumno['last_name'] = 'apellido2 2'

nuevo_profesor = {}
nuevo_profesor['username'] = 'nuevo_profesor@ejemplo2.ugr.es'
nuevo_profesor['first_name'] = 'profesorapellido2 1'
nuevo_profesor['last_name'] = 'profesorapellido2 2'
nuevo_profesor['departamento'] = 'profesordepartamento2'

###################   PROPUESTA   ########################
#Usar como username que es unico el email de la ugr


class TfgTests(TestCase):

    def setUp(self):

        self.alumn1_username = 'alumn1@correo.ugr.es'
        self.alumn1_nombre = 'alumno'
        self.alumn1_apellidos = 'apellido 1 apellido 2'

        self.prof1_username = 'prof1@ejemplo2.ugr.es'
        self.prof1_nombre = 'prof1'
        self.prof1_apellidos = 'profesorapellido2 1 profesorapellido2 2'
        self.prof1_departamento = 'profesordepartamento1'

        Alumno.objects.create_user(username=self.alumn1_username, first_name= self.alumn1_nombre,last_name= self.alumn1_apellidos)
        Profesor.objects.create_user(username=self.prof1_username, first_name= self.prof1_nombre,last_name= self.prof1_apellidos, departamento= self.prof1_departamento)

    def test_create_alumno(self):

        alumno = Alumno(username=self.alumn1_username, first_name= self.alumn1_nombre,last_name= self.alumn1_apellidos)
        self.assertNotEqual(alumno, None)

    def test_check_alumno(self):
        alumno = Alumno.objects.get(username=self.alumn1_username)

        self.assertEqual(alumno.username, self.alumn1_username)
        self.assertEqual(alumno.first_name, self.alumn1_nombre)
        self.assertEqual(alumno.last_name, self.alumn1_apellidos)

    def test_create_profesor(self):

        profesor = Profesor(username=self.prof1_username, first_name= self.prof1_nombre,last_name= self.prof1_apellidos, departamento= self.prof1_departamento)
        self.assertNotEqual(profesor, None)

    def test_check_profesor(self):
        profesor = Profesor.objects.get(username=self.prof1_username)

        self.assertEqual(profesor.username, self.prof1_username)
        self.assertEqual(profesor.first_name, self.prof1_nombre)
        self.assertEqual(profesor.last_name, self.prof1_apellidos)
        self.assertEqual(profesor.departamento, self.prof1_departamento)

    def test_update_alumno(self):

        alumno = Alumno.objects.get(username=self.alumn1_username)
        alumno.username = nuevo_alumno['username']
        alumno.first_name = nuevo_alumno['first_name']
        alumno.last_name = nuevo_alumno['last_name']

        alumno.save()

        new_alumno = Alumno.objects.get(username=alumno.username)

        self.assertEqual(alumno.username, new_alumno.username)
        self.assertEqual(alumno.first_name, new_alumno.first_name)
        self.assertEqual(alumno.last_name, new_alumno.last_name)
        self.assertEqual(alumno.email, new_alumno.email)

    def test_update_profesores(self):

        profesor = Profesor.objects.get(username=self.prof1_username)
        profesor.username = nuevo_profesor['username']
        profesor.first_name = nuevo_profesor['first_name']
        profesor.last_name = nuevo_profesor['last_name']
        profesor.departamento = nuevo_profesor['departamento']

        profesor.save()

        new_profesor = Profesor.objects.get(username=profesor.username)

        self.assertEqual(profesor.username, new_profesor.username)
        self.assertEqual(profesor.first_name, new_profesor.first_name)
        self.assertEqual(profesor.last_name, new_profesor.last_name)
        self.assertEqual(profesor.email, new_profesor.email)
        self.assertEqual(profesor.departamento, new_profesor.departamento)

    def test_delete_alumno(self):

        alumno = Alumno.objects.get(username=self.alumn1_username)
        alumno.delete()

        try:
            alumno = Alumno.objects.get(username=self.alumn1_username)
        except Alumno.DoesNotExist:
            alumno = None

        self.assertEqual(alumno, None)

    def test_delete_profesor(self):

        profesor = Profesor.objects.get(username=self.prof1_username)
        profesor.delete()

        try:
            profesor = Profesor.objects.get(username=self.prof1_username)
        except Profesor.DoesNotExist:
            profesor = None

        self.assertEqual(profesor, None)