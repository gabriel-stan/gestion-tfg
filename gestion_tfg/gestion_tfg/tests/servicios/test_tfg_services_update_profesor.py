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
        self.prof1_departamento = 'departamento primero'

        self.otro_username = 'ejemplo2@ugr.es'
        self.otro_nombre = 'profesor 2'
        self.otro_apellidos = 'apellido 2 apellido 22'
        self.otro_departamento = 'otro departamento'

        self.new_username = 'ejemplo3@ugr.es'
        self.new_nombre = 'profesor 3'
        self.new_apellidos = 'apellido 3 apellido 33'
        self.new_departamento = 'departamento nuevo'

        self.prof1 = tfg_services.insert_profesor(Profesor(username=self.prof1_username, first_name=self.prof1_nombre,
                                                           last_name=self.prof1_apellidos,
                                                           departamento=self.prof1_departamento))['data']

        self.prof2 = tfg_services.insert_profesor(Profesor(username=self.otro_username, first_name=self.otro_nombre,
                                                           last_name=self.otro_apellidos,
                                                           departamento=self.otro_departamento))['data']


    def test_update_profesor_username(self):

        #username vacio
        campos = dict(username='')
        result = tfg_services.update_profesor(self.prof1, campos)
        self.assertEqual(result['status'], False)

        #username no string
        campos = dict(username=2)
        result = tfg_services.update_profesor(self.prof1, campos)
        self.assertEqual(result['status'], False)

        #username no valido
        campos = dict(username='usuario@correo.ugr.es')
        result = tfg_services.update_profesor(self.prof1, campos)
        self.assertEqual(result['status'], False)

        #username repetido
        campos = dict(username=self.otro_username)
        result = tfg_services.update_profesor(self.prof1, campos)
        self.assertEqual(result['status'], False)

        #username valido
        campos = dict(username='usuario_nuevo@ugr.es')
        result = tfg_services.update_profesor(self.prof1, campos)
        self.assertEqual(result['data'].username, campos['username'])
        
    def test_update_profesor_nombre(self):

        #first_name vacio
        campos = dict(first_name='')
        result = tfg_services.update_profesor(self.prof1, campos)
        self.assertEqual(result['status'], False)

        #first_name no string
        campos = dict(first_name=1)
        result = tfg_services.update_profesor(self.prof1, campos)
        self.assertEqual(result['status'], False)

        #first_name valido
        campos = dict(first_name='Pacopepe')
        result = tfg_services.update_profesor(self.prof1, campos)
        self.assertEqual(result['data'].first_name, campos['first_name'])


    def test_update_profesor_apellidos(self):

        #last_name vacio
        campos = dict(last_name='')
        result = tfg_services.update_profesor(self.prof1, campos)
        self.assertEqual(result['status'], False)

        #last_name no string
        campos = dict(last_name=1)
        result = tfg_services.update_profesor(self.prof1, campos)
        self.assertEqual(result['status'], False)

        #last_name valido
        campos = dict(last_name='Pacopepe Federico')
        result = tfg_services.update_profesor(self.prof1, campos)
        self.assertEqual(result['data'].last_name, campos['last_name'])

    def test_update_profesor_departamento(self):

        #last_name vacio
        campos = dict(departamento='')
        result = tfg_services.update_profesor(self.prof1, campos)
        self.assertEqual(result['status'], False)

        #last_name no string
        campos = dict(departamento=1)
        result = tfg_services.update_profesor(self.prof1, campos)
        self.assertEqual(result['status'], False)

        #last_name valido
        campos = dict(departamento='departemento segundo')
        result = tfg_services.update_profesor(self.prof1, campos)
        self.assertEqual(result['data'].departamento, campos['departamento'])

    def test_update_profesor_valido(self):

        campos = dict(username=self.new_username, first_name=self.new_nombre, last_name=self.new_apellidos)
        result = tfg_services.update_profesor(self.prof1, campos)
        self.assertEqual(result['data'].username, self.new_username)
