from django.test import TestCase

from controller.servicios import tfg_services
from model.models import Alumno


###################   PROPUESTA   ########################
#Usar como username que es unico el email de la ugr

class TfgServicesTests(TestCase):
    def setUp(self):

        self.alumn1_username = 'ejemplo@correo.ugr.es'
        self.alumn1_nombre = 'alumno 1'
        self.alumn1_apellidos = 'apellido 1 apellido 12'

        self.otro_username = 'ejemplo2@correo.ugr.es'
        self.otro_nombre = 'alumno 2'
        self.otro_apellidos = 'apellido 2 apellido 22'

        self.new_username = 'ejemplo3@correo.ugr.es'
        self.new_nombre = 'alumno 3'
        self.new_apellidos = 'apellido 3 apellido 33'

        self.alumno1 = tfg_services.insert_alumno(Alumno(username=self.alumn1_username, first_name=self.alumn1_nombre,
                                                         last_name=self.alumn1_apellidos))['data']

        self.alumno2 = tfg_services.insert_alumno(Alumno(username=self.otro_username, first_name=self.otro_nombre,
                                                         last_name=self.otro_apellidos))['data']


    def test_update_alumno_username(self):

        #username vacio
        campos = dict(username='')
        result = tfg_services.update_alumno(self.alumno1, campos)
        self.assertEqual(result['status'], False)

        #username no string
        campos = dict(username=2)
        result = tfg_services.update_alumno(self.alumno1, campos)
        self.assertEqual(result['status'], False)

        #username no valido
        campos = dict(username='usuario@ugr.es')
        result = tfg_services.update_alumno(self.alumno1, campos)
        self.assertEqual(result['status'], False)

        #username repetido
        campos = dict(username=self.otro_username)
        result = tfg_services.update_alumno(self.alumno1, campos)
        self.assertEqual(result['status'], False)

        #username valido
        campos = dict(username='usuario_nuevo@correo.ugr.es')
        result = tfg_services.update_alumno(self.alumno1, campos)
        self.assertEqual(result['data'].username, campos['username'])
        
    def test_update_alumno_nombre(self):

        #first_name vacio
        campos = dict(first_name='')
        result = tfg_services.update_alumno(self.alumno1, campos)
        self.assertEqual(result['status'], False)

        #first_name no string
        campos = dict(first_name=1)
        result = tfg_services.update_alumno(self.alumno1, campos)
        self.assertEqual(result['status'], False)

        #first_name valido
        campos = dict(first_name='Pacopepe')
        result = tfg_services.update_alumno(self.alumno1, campos)
        self.assertEqual(result['data'].first_name, campos['first_name'])


    def test_update_alumno_apellidos(self):

        campos = dict(last_name='')
        result = tfg_services.update_alumno(self.alumno1, campos)
        self.assertEqual(result['status'], False)

        campos = dict(last_name=1)
        result = tfg_services.update_alumno(self.alumno1, campos)
        self.assertEqual(result['status'], False)

        campos = dict(last_name='Pacopepe Federico')
        result = tfg_services.update_alumno(self.alumno1, campos)
        self.assertEqual(result['data'].last_name, campos['last_name'])

    def test_update_alumno_valido(self):

        campos = dict(username=self.new_username, first_name=self.new_nombre, last_name=self.new_apellidos)
        result = tfg_services.update_alumno(self.alumno1, campos)
        self.assertEqual(result['data'].username, self.new_username)
