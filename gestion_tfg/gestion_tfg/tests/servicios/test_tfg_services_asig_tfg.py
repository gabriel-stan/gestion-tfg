from django.test import TestCase
from gestion_tfg.models import Tfg, Tfg_Asig
from django.contrib.auth.models import User

from gestion_tfg.servicios import tfg_services


class TfgServicesTests(TestCase):
    def setUp(self):

        self.tipo_tfg = 'tipo1'
        self.titulo_tfg = 'titulo1'
        self.n_alumnos_tfg = 2
        self.descripcion_tfg = 'descripcion'
        self.conocimientos_previos_tfg = 'conocimientos previos'
        self.hard_soft_tfg = 'hardware software'

        self.user_tutor_tfg = User.objects.create_user(
            username='pepe', email='pepe@ugr.es', password='top_secret')
        self.user_cotutor_tfg = User.objects.create_user(
            username='paco', email='paco@ugr.es', password='top_secret')

        self.tfg = Tfg.objects.create(tipo=self.tipo_tfg, titulo=self.titulo_tfg,
                           n_alumnos=self.n_alumnos_tfg, descripcion=self.descripcion_tfg,
                           conocimientos_previos=self.conocimientos_previos_tfg,
                           hard_soft=self.hard_soft_tfg, tutor=self.user_tutor_tfg,
                           cotutor=self.user_cotutor_tfg)

        self.user_alumn1_tfg = User.objects.create_user(
            username='alumn1', email='alumn1@ugr.es', password='top_secretalumn1')
        self.user_alumn2_tfg = User.objects.create_user(
            username='alumn2', email='alumn2@ugr.es', password='top_secretalumn2')
        self.user_alumn3_tfg = User.objects.create_user(
            username='alumn3', email='alumn3@ugr.es', password='top_secretalumn3')

        self.otro_tipo_tfg = 'otro tipo'
        self.otro_titulo_tfg = 'otro titulo'
        self.otro_n_alumnos_tfg = 3
        self.otro_descripcion_tfg = 'otra descripcion'
        self.otro_conocimientos_previos_tfg = 'otros conocimientos previos'
        self.otro_hard_soft_tfg = 'otros hardware y software'

        self.otro_user_tutor_tfg = User.objects.create_user(
            username='manuel', email='manuel@ugr.es', password='top_secret')
        self.otro_user_cotutor_tfg = User.objects.create_user(
            username='manolo', email='manolo@ugr.es', password='top_secret')

        self.otro_user_alumn1_tfg = User.objects.create_user(
            username='otro_alumn1', email='otro_alumn1@ugr.es', password='otro_top_secretalumn1')
        self.otro_user_alumn2_tfg = User.objects.create_user(
            username='otro_alumn2', email='otro_alumn2@ugr.es', password='otro_top_secretalumn2')
        self.otro_user_alumn3_tfg = User.objects.create_user(
            username='otro_alumn3', email='otro_alumn3@ugr.es', password='otro_top_secretalumn3')

        self.otro_tfg = Tfg.objects.create(tipo=self.otro_tipo_tfg, titulo=self.otro_titulo_tfg,
                   n_alumnos=self.otro_n_alumnos_tfg, descripcion=self.otro_descripcion_tfg,
                   conocimientos_previos=self.conocimientos_previos_tfg,
                   hard_soft=self.otro_hard_soft_tfg, tutor=self.otro_user_tutor_tfg,
                   cotutor=self.otro_user_cotutor_tfg)

    def test_asig_tfg_tfg_error(self):

        tfg = "tfg"
        result = tfg_services.asignar_tfg(tfg, self.user_alumn1_tfg, self.user_alumn2_tfg, self.user_alumn3_tfg)
        self.assertEqual(result, False)

    def test_asig_tfg_alumno_error(self):

        alumno1 = "alumno"
        tfg = Tfg.objects.get(titulo=self.titulo_tfg)
        result = tfg_services.asignar_tfg(tfg, alumno1, self.user_alumn2_tfg, self.user_alumn3_tfg)
        self.assertEqual(result, False)

    def test_asig_tfg_ya_asig(self):

        tfg = Tfg.objects.get(titulo=self.titulo_tfg)
        tfg_services.asignar_tfg(tfg, self.user_alumn1_tfg, self.user_alumn2_tfg, self.user_alumn3_tfg)
        result = tfg_services.asignar_tfg(tfg, self.user_alumn1_tfg, self.user_alumn2_tfg, self.user_alumn3_tfg)
        self.assertEqual(result, False)

    def test_asig_tfg_alumnos(self):

        tfg = Tfg.objects.get(titulo=self.titulo_tfg)
        result = tfg_services.asignar_tfg(tfg, self.user_alumn1_tfg, self.user_alumn2_tfg, self.user_alumn3_tfg)
        self.assertEqual(result, True)
        #Alumno1 ya tiene tfg
        otro_tfg = Tfg.objects.get(titulo=self.otro_titulo_tfg)
        result = tfg_services.asignar_tfg(otro_tfg, self.user_alumn1_tfg)
        self.assertEqual(result, False)
        #Alumno2 ya tiene tfg
        result = tfg_services.asignar_tfg(otro_tfg, self.otro_user_alumn1_tfg, self.user_alumn2_tfg)
        self.assertEqual(result, False)
        #Alumno3 ya tiene tfg
        result = tfg_services.asignar_tfg(otro_tfg, self.otro_user_alumn1_tfg, self.otro_user_alumn2_tfg, self.user_alumn3_tfg)
        self.assertEqual(result, False)
        #Nuevo Tfg y nuevos alumnos
        result = tfg_services.asignar_tfg(otro_tfg, self.otro_user_alumn1_tfg, self.otro_user_alumn2_tfg, self.otro_user_alumn3_tfg)
        self.assertEqual(result, True)
