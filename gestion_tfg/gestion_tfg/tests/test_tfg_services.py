from django.test import TestCase
from gestion_tfg.models import Tfg
from django.contrib.auth.models import User

from gestion_tfg.servicios import tfg_services


class TfgServicesTests(TestCase):
    def setUp(self):

        self.tipo_tfg = 'tipo1'
        self.titulo_tfg = 'titulo1'
        self.otro_titulo_tfg = 'titulo2'
        self.n_alumnos_tfg = 2
        self.descripcion_tfg = 'descripcion'
        self.conocimientos_previos_tfg = 'conocimientos previos'
        self.hard_soft_tfg = 'hardware software'

        self.user_tutor_tfg = User.objects.create_user(
            username='pepe', email='pepe@ugr.es', password='top_secret')
        self.user_cotutor_tfg = User.objects.create_user(
            username='paco', email='paco@ugr.es', password='top_secret')

        self.tfg1 = Tfg(tipo=self.tipo_tfg, titulo=self.titulo_tfg,
                   n_alumnos=self.n_alumnos_tfg, descripcion=self.descripcion_tfg,
                   conocimientos_previos=self.conocimientos_previos_tfg,
                   hard_soft=self.hard_soft_tfg, tutor=self.user_tutor_tfg,
                   cotutor=self.user_cotutor_tfg)

        # insertamos un tfg valido
        tfg_services.insert_tfg(self.tfg1)

    def test_insert_tfg_vacio(self):

        tfg = Tfg()
        result = tfg_services.insert_tfg(tfg)
        self.assertEqual(result, False)

    def test_insert_tfg_correcto(self):

        tfg = Tfg(tipo=self.tipo_tfg, titulo=self.otro_titulo_tfg,
                   n_alumnos=self.n_alumnos_tfg, descripcion=self.descripcion_tfg,
                   conocimientos_previos=self.conocimientos_previos_tfg,
                   hard_soft=self.hard_soft_tfg, tutor=self.user_tutor_tfg,
                   cotutor=self.user_cotutor_tfg)
        result = tfg_services.insert_tfg(tfg)
        self.assertEqual(result, True)

    def test_tfg_titulo(self):

        #sin titulo
        tfg = Tfg(tipo=self.tipo_tfg,
                   n_alumnos=self.n_alumnos_tfg, descripcion=self.descripcion_tfg,
                   conocimientos_previos=self.conocimientos_previos_tfg,
                   hard_soft=self.hard_soft_tfg, tutor=self.user_tutor_tfg,
                   cotutor=self.user_cotutor_tfg)

        result = tfg_services.insert_tfg(tfg)
        self.assertEqual(result, False)

        #tfg con titulo duplicado - no deberia pasar
        tfg = Tfg(tipo=self.tipo_tfg, titulo=self.titulo_tfg,
                   n_alumnos=self.n_alumnos_tfg, descripcion=self.descripcion_tfg,
                   conocimientos_previos=self.conocimientos_previos_tfg,
                   hard_soft=self.hard_soft_tfg, tutor=self.user_tutor_tfg,
                   cotutor=self.user_cotutor_tfg)

        result = tfg_services.insert_tfg(tfg)
        self.assertEqual(result, False)

        #tfg con otro titulo
        tfg = Tfg(tipo=self.tipo_tfg, titulo=self.otro_titulo_tfg,
                   n_alumnos=self.n_alumnos_tfg, descripcion=self.descripcion_tfg,
                   conocimientos_previos=self.conocimientos_previos_tfg,
                   hard_soft=self.hard_soft_tfg, tutor=self.user_tutor_tfg,
                   cotutor=self.user_cotutor_tfg)

        result = tfg_services.insert_tfg(tfg)
        self.assertEqual(result, True)

    def test_tfg_tipo(self):

        #tfg sin tipo
        tfg = Tfg(titulo=self.otro_titulo_tfg,
                   n_alumnos=self.n_alumnos_tfg, descripcion=self.descripcion_tfg,
                   conocimientos_previos=self.conocimientos_previos_tfg,
                   hard_soft=self.hard_soft_tfg, tutor=self.user_tutor_tfg,
                   cotutor=self.user_cotutor_tfg)

        result = tfg_services.insert_tfg(tfg)
        self.assertEqual(result, False)

    def test_tfg_n_alumnos(self):

        #tfg sin numero de alumnos
        tfg = Tfg(tipo=self.tipo_tfg, titulo=self.otro_titulo_tfg,
                   descripcion=self.descripcion_tfg,
                   conocimientos_previos=self.conocimientos_previos_tfg,
                   hard_soft=self.hard_soft_tfg, tutor=self.user_tutor_tfg,
                   cotutor=self.user_cotutor_tfg)

        result = tfg_services.insert_tfg(tfg)
        self.assertEqual(result, False)

    def test_tfg_n_alumnos_menor(self):

        #tfg con menos de 1 alumno
        tfg = Tfg(tipo=self.tipo_tfg, titulo=self.otro_titulo_tfg,
                   n_alumnos=-1, descripcion=self.descripcion_tfg,
                   conocimientos_previos=self.conocimientos_previos_tfg,
                   hard_soft=self.hard_soft_tfg, tutor=self.user_tutor_tfg,
                   cotutor=self.user_cotutor_tfg)

        result = tfg_services.insert_tfg(tfg)
        self.assertEqual(result, False)

    def test_tfg_n_alumnos_mayor(self):

        #tfg con mas de 3 alumnos
        tfg = Tfg(tipo=self.tipo_tfg, titulo=self.otro_titulo_tfg,
                   n_alumnos=4, descripcion=self.descripcion_tfg,
                   conocimientos_previos=self.conocimientos_previos_tfg,
                   hard_soft=self.hard_soft_tfg, tutor=self.user_tutor_tfg,
                   cotutor=self.user_cotutor_tfg)

        result = tfg_services.insert_tfg(tfg)
        self.assertEqual(result, False)

    def test_tfg_descripcion(self):

        #tfg sin descripcion
        tfg = Tfg(tipo=self.tipo_tfg, titulo=self.otro_titulo_tfg,
                   n_alumnos=self.n_alumnos_tfg,
                   conocimientos_previos=self.conocimientos_previos_tfg,
                   hard_soft=self.hard_soft_tfg, tutor=self.user_tutor_tfg,
                   cotutor=self.user_cotutor_tfg)

        result = tfg_services.insert_tfg(tfg)
        self.assertEqual(result, False)

    def test_tfg_conocimientos_previos(self):

        #tfg sin conocimientos previos
        tfg = Tfg(tipo=self.tipo_tfg, titulo=self.otro_titulo_tfg,
                   n_alumnos=self.n_alumnos_tfg, descripcion=self.descripcion_tfg,
                   #conocimientos_previos=self.conocimientos_previos_tfg,
                   hard_soft=self.hard_soft_tfg, tutor=self.user_tutor_tfg,
                   cotutor=self.user_cotutor_tfg)
        result = tfg_services.insert_tfg(tfg)
        self.assertEqual(result, False)

    def test_tfg_hard_soft(self):

        #tfg sin requisitos hardware/software
        tfg = Tfg(tipo=self.tipo_tfg, titulo=self.otro_titulo_tfg,
                   n_alumnos=self.n_alumnos_tfg, descripcion=self.descripcion_tfg,
                   conocimientos_previos=self.conocimientos_previos_tfg,
                   #hard_soft=self.hard_soft_tfg,
                   tutor=self.user_tutor_tfg,
                   cotutor=self.user_cotutor_tfg)
        result = tfg_services.insert_tfg(tfg)
        self.assertEqual(result, False)

    def test_tfg_tutor(self):

        #tfg sin tutor
        tfg = Tfg(tipo=self.tipo_tfg, titulo=self.otro_titulo_tfg,
                   n_alumnos=self.n_alumnos_tfg, descripcion=self.descripcion_tfg,
                   conocimientos_previos=self.conocimientos_previos_tfg,
                   hard_soft=self.hard_soft_tfg,
                   #tutor=self.user_tutor_tfg,
                   cotutor=self.user_cotutor_tfg)
        result = tfg_services.insert_tfg(tfg)
        self.assertEqual(result, False)

    def test_tfg_cotutor(self):

        #tfg sin cotutor
        tfg = Tfg(tipo=self.tipo_tfg, titulo=self.otro_titulo_tfg,
                   n_alumnos=self.n_alumnos_tfg, descripcion=self.descripcion_tfg,
                   conocimientos_previos=self.conocimientos_previos_tfg,
                   hard_soft=self.hard_soft_tfg,
                   tutor=self.user_tutor_tfg,
                   #cotutor=self.user_cotutor_tfg
                   )
        result = tfg_services.insert_tfg(tfg)
        self.assertEqual(result, False)
