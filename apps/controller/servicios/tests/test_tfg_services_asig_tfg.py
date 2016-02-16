from django.contrib.auth.models import Group
from django.test import TestCase

from controller.servicios import tfg_services
from model.models import Tfg, Profesor, Alumno


class TfgServicesTests(TestCase):
    def setUp(self):

        self.tipo_tfg = 'tipo1'
        self.titulo_tfg = 'titulo1'
        self.n_alumnos_tfg = 2
        self.descripcion_tfg = 'descripcion'
        self.conocimientos_previos_tfg = 'conocimientos previos'
        self.hard_soft_tfg = 'hardware software'

        self.user_tutor_tfg = Profesor.objects.create_user(
            username='pepe', email='pepe@ugr.es', password='top_secret')
        self.user_cotutor_tfg = Profesor.objects.create_user(
            username='paco', email='paco@ugr.es', password='top_secret')

        self.tfg = Tfg.objects.create(tipo=self.tipo_tfg, titulo=self.titulo_tfg,
                           n_alumnos=self.n_alumnos_tfg, descripcion=self.descripcion_tfg,
                           conocimientos_previos=self.conocimientos_previos_tfg,
                           hard_soft=self.hard_soft_tfg, tutor=self.user_tutor_tfg,
                           cotutor=self.user_cotutor_tfg)

        self.user_alumn1_tfg = tfg_services.insert_alumno(Alumno(username='alumn1@correo.ugr.es', first_name='alumn1',
                                                                 last_name='apellidos 1'))['data']
        self.user_alumn2_tfg = tfg_services.insert_alumno(Alumno(username='alumn2@correo.ugr.es', first_name='alumn2',
                                                                 last_name='apellidos 2'))['data']
        self.user_alumn3_tfg = tfg_services.insert_alumno(Alumno(username='alumn3@correo.ugr.es', first_name='alumn3',
                                                                 last_name='apellidos 3'))['data']
        self.otro_user_alumn1_tfg = tfg_services.insert_alumno(Alumno(username='otro_alumn1@correo.ugr.es', first_name='otro_alumn1',
                                                                      last_name='otro_apellidos 1'))['data']
        self.otro_user_alumn2_tfg = tfg_services.insert_alumno(Alumno(username='otro_alumn2@correo.ugr.es', first_name='otro_alumn2',
                                                                      last_name='otro_apellidos 2'))['data']
        self.otro_user_alumn3_tfg = tfg_services.insert_alumno(Alumno(username='otro_alumn3@correo.ugr.es', first_name='otro_alumn3',
                                                                      last_name='otro_apellidos 3'))['data']

        self.otro_tipo_tfg = 'otro tipo'
        self.otro_titulo_tfg = 'otro titulo'
        self.otro_n_alumnos_tfg = 3
        self.otro_descripcion_tfg = 'otra descripcion'
        self.otro_conocimientos_previos_tfg = 'otros conocimientos previos'
        self.otro_hard_soft_tfg = 'otros hardware y software'


        self.otro_user_tutor_tfg = tfg_services.insert_profesor(Profesor(username='manuel@ugr.es',
                                                                         first_name='prof 1',
                                                                         last_name='apellidos 1',
                                                                         departamento='departamento 1'))['data']

        self.otro_user_cotutor_tfg = tfg_services.insert_profesor(Profesor(username='comanuel@ugr.es',
                                                                           first_name='prof 2',
                                                                           last_name='apellidos 2',
                                                                           departamento='departamento 1'))['data']

        self.otro_tfg = Tfg.objects.create(tipo=self.otro_tipo_tfg, titulo=self.otro_titulo_tfg,
                   n_alumnos=self.otro_n_alumnos_tfg, descripcion=self.otro_descripcion_tfg,
                   conocimientos_previos=self.conocimientos_previos_tfg,
                   hard_soft=self.otro_hard_soft_tfg, tutor=self.otro_user_tutor_tfg,
                   cotutor=self.otro_user_cotutor_tfg)

        self.grupo_profesores = Group.objects.get_or_create(name='Profesores')
        self.grupo_alumnos = Group.objects.get_or_create(name='Alumnos')

    def test_asig_tfg_tfg_error(self):

        tfg = "tfg"
        result = tfg_services.asignar_tfg(tfg, self.user_alumn1_tfg, self.user_alumn2_tfg, self.user_alumn3_tfg)
        self.assertEqual(result['status'], False)

    def test_asig_tfg_alumno_error(self):

        alumno1 = "alumno"
        tfg = Tfg.objects.get(titulo=self.titulo_tfg)
        result = tfg_services.asignar_tfg(tfg, alumno1, self.user_alumn2_tfg, self.user_alumn3_tfg)
        self.assertEqual(result['status'], False)

        #Alumno 2 y 3 no pertenecen al grupo de alumnos
        self.user_alumn1_tfg.groups.add(self.grupo_alumnos[0])
        result = tfg_services.asignar_tfg(tfg, self.user_alumn1_tfg, self.user_alumn2_tfg, self.user_alumn3_tfg)
        self.assertEqual(result['status'], False)

        #Alumno 1 y 3 no pertenecen al grupo de alumnos
        self.user_alumn2_tfg.groups.add(self.grupo_alumnos[0])
        result = tfg_services.asignar_tfg(tfg, self.user_alumn1_tfg, self.user_alumn2_tfg, self.user_alumn3_tfg)
        self.assertEqual(result['status'], False)

        #Alumno 1 y 3 no pertenecen al grupo de alumnos
        self.user_alumn2_tfg.groups.remove(self.grupo_alumnos[0])
        self.user_alumn3_tfg.groups.add(self.grupo_alumnos[0])
        result = tfg_services.asignar_tfg(tfg, self.user_alumn1_tfg, self.user_alumn2_tfg, self.user_alumn3_tfg)
        self.assertEqual(result['status'], False)

    def test_asig_tfg_ya_asig(self):

        tfg = Tfg.objects.get(titulo=self.titulo_tfg)
        tfg_services.asignar_tfg(tfg, self.user_alumn1_tfg, self.user_alumn2_tfg, self.user_alumn3_tfg)
        result = tfg_services.asignar_tfg(tfg, self.user_alumn1_tfg, self.user_alumn2_tfg, self.user_alumn3_tfg)
        self.assertEqual(result['status'], False)

    def test_asig_tfg_alumnos(self):

        self.user_alumn1_tfg.groups.add(self.grupo_alumnos[0])
        self.user_alumn2_tfg.groups.add(self.grupo_alumnos[0])
        self.user_alumn3_tfg.groups.add(self.grupo_alumnos[0])
        self.otro_user_alumn1_tfg.groups.add(self.grupo_alumnos[0])
        self.otro_user_alumn2_tfg.groups.add(self.grupo_alumnos[0])
        self.otro_user_alumn3_tfg.groups.add(self.grupo_alumnos[0])

        tfg = Tfg.objects.get(titulo=self.titulo_tfg)
        result = tfg_services.asignar_tfg(tfg, self.user_alumn1_tfg, self.user_alumn2_tfg, self.user_alumn3_tfg)
        self.assertEqual(result['status'], True)

        #Alumno1 ya tiene tfg
        otro_tfg = Tfg.objects.get(titulo=self.otro_titulo_tfg)
        result = tfg_services.asignar_tfg(otro_tfg, self.user_alumn1_tfg)
        self.assertEqual(result['status'], False)

        #Alumno2 ya tiene tfg
        result = tfg_services.asignar_tfg(otro_tfg, self.otro_user_alumn1_tfg, self.user_alumn2_tfg)
        self.assertEqual(result['status'], False)

        #Alumno3 ya tiene tfg
        result = tfg_services.asignar_tfg(otro_tfg, self.otro_user_alumn1_tfg, self.otro_user_alumn2_tfg, self.user_alumn3_tfg)
        self.assertEqual(result['status'], False)

        #Nuevo Tfg y nuevos alumnos
        result = tfg_services.asignar_tfg(otro_tfg, self.otro_user_alumn1_tfg, self.otro_user_alumn2_tfg, self.otro_user_alumn3_tfg)
        self.assertEqual(result['status'], True)
