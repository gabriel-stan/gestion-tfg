from django.test import TestCase
from gestion_tfg.models import Alumno, Profesor

nuevo_alumno = {}
nuevo_alumno['username'] = 'alumno 2'
nuevo_alumno['first_name'] = 'apellido2 1'
nuevo_alumno['last_name'] = 'apellido2 2'
nuevo_alumno['email'] = 'descripcion2'
nuevo_alumno['dni'] = '2ejemplo@ejemplo.ugr.es'

nuevo_profesor = {}
nuevo_profesor['username'] = 'profesor2 1'
nuevo_profesor['first_name'] = 'profesorapellido2 1'
nuevo_profesor['last_name'] = 'profesorapellido2 2'
nuevo_profesor['email'] = 'profesorejemplo2@ejemplo2.ugr.es'
nuevo_profesor['departamento'] = 'profesordepartamento2'

class TfgTests(TestCase):

    def setUp(self):

        self.alumn1_nombre = 'alumno 1'
        self.alumn1_apellido1 = 'apellido 1'
        self.alumn1_apellido2 = 'apellido 2'
        self.alumn1_dni = '12467249S'
        self.alumn1_email = 'ejemplo@ejemplo.ugr.es'

        self.alumn1_nombre_nuevo = 'alumno 2'
        self.alumn1_apellido1_nuevo = 'apellido2 1'
        self.alumn1_apellido2_nuevo = 'apellido2 2'
        self.alumn1_dni_nuevo = '22467249S'
        self.alumn1_email_nuevo = '2ejemplo@ejemplo.ugr.es'

        self.prof1_nombre = 'profesor 1'
        self.prof1_apellido1 = 'profesorapellido2 1'
        self.prof1_apellido2 = 'profesorapellido2 2'
        self.prof1_departamento = 'profesordepartamento1'
        self.prof1_email = 'profesorejemplo2@ejemplo2.ugr.es'
        self.prof1_apellido1 = 'profesorpass2'


        Alumno.objects.create_user(username=self.alumn1_nombre, first_name= self.alumn1_apellido1,last_name= self.alumn1_apellido2,email= self.alumn1_email, dni= self.alumn1_dni)
        Profesor.objects.create_user(username=self.prof1_nombre, first_name= self.prof1_apellido1,last_name= self.prof1_apellido2,email= self.prof1_email, departamento= self.prof1_departamento)

    def test_create_alumno(self):

        alumno = Alumno(username=self.alumn1_nombre, first_name= self.alumn1_apellido1,last_name= self.alumn1_apellido2,email= self.alumn1_email, dni= self.alumn1_dni)
        self.assertNotEqual(alumno, None)

    def test_check_alumno(self):
        alumno = Alumno.objects.get(username=self.alumn1_nombre)

        self.assertEqual(alumno.username, self.alumn1_nombre)
        self.assertEqual(alumno.first_name, self.alumn1_apellido1)
        self.assertEqual(alumno.last_name, self.alumn1_apellido2)
        self.assertEqual(alumno.email, self.alumn1_email)
        self.assertEqual(alumno.dni, self.alumn1_dni)

    def test_create_profesor(self):

        profesor = Profesor(username=self.prof1_nombre, first_name= self.prof1_apellido1,last_name= self.prof1_apellido2,email= self.prof1_email, departamento= self.prof1_departamento)
        self.assertNotEqual(profesor, None)

    def test_check_profesor(self):
        profesor = Profesor.objects.get(username=self.prof1_nombre)

        self.assertEqual(profesor.username, self.prof1_nombre)
        self.assertEqual(profesor.first_name, self.prof1_apellido1)
        self.assertEqual(profesor.last_name, self.prof1_apellido2)
        self.assertEqual(profesor.email, self.prof1_email)
        self.assertEqual(profesor.departamento, self.prof1_departamento)

    def test_update_alumno(self):

        alumno = Alumno.objects.get(username=self.alumn1_nombre)
        alumno.username = nuevo_alumno['username']
        alumno.first_name = nuevo_alumno['first_name']
        alumno.last_name = nuevo_alumno['last_name']
        alumno.email = nuevo_alumno['email']
        alumno.dni = nuevo_alumno['dni']

        alumno.save()

        new_alumno = Alumno.objects.get(username=alumno.username)

        self.assertEqual(alumno.username, new_alumno.username)
        self.assertEqual(alumno.first_name, new_alumno.first_name)
        self.assertEqual(alumno.last_name, new_alumno.last_name)
        self.assertEqual(alumno.email, new_alumno.email)
        self.assertEqual(alumno.dni, new_alumno.dni)

    def test_update_profesores(self):

        profesor = Profesor.objects.get(username=self.prof1_nombre)
        profesor.username = nuevo_profesor['username']
        profesor.first_name = nuevo_profesor['first_name']
        profesor.last_name = nuevo_profesor['last_name']
        profesor.email = nuevo_profesor['email']
        profesor.departamento = nuevo_profesor['departamento']

        profesor.save()

        new_profesor = Profesor.objects.get(username=profesor.username)

        self.assertEqual(profesor.username, new_profesor.username)
        self.assertEqual(profesor.first_name, new_profesor.first_name)
        self.assertEqual(profesor.last_name, new_profesor.last_name)
        self.assertEqual(profesor.email, new_profesor.email)
        self.assertEqual(profesor.departamento, new_profesor.departamento)

    def test_delete_alumno(self):

        alumno = Alumno.objects.get(username=self.alumn1_nombre)
        alumno.delete()

        try:
            alumno = Alumno.objects.get(username=self.alumn1_nombre)
        except Alumno.DoesNotExist:
            alumno = None

        self.assertEqual(alumno, None)

    def test_delete_profesor(self):

        profesor = Profesor.objects.get(username=self.prof1_nombre)
        profesor.delete()

        try:
            profesor = Profesor.objects.get(username=self.prof1_nombre)
        except Profesor.DoesNotExist:
            profesor = None

        self.assertEqual(profesor, None)