from django.test import TestCase
from gestion_tfg.models import Tfg
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

    def test_insert_tfg_vacio(self):

        tfg1 = Tfg(tipo=self.tipo_tfg, titulo=self.titulo_tfg,
                   n_alumnos=self.n_alumnos_tfg, descripcion=self.descripcion_tfg,
                   conocimientos_previos=self.conocimientos_previos_tfg,
                   hard_soft=self.hard_soft_tfg, tutor=self.user_tutor_tfg,
                   cotutor=self.user_cotutor_tfg)

        #TFG vacio
        tfg = Tfg()
        result = tfg_services.insert_tfg(tfg)
        self.assertEqual(result, False)


    def test_tfg_titulo(self):
        tfg = Tfg()
        result = tfg_services.insert_tfg(tfg)
        self.assertEqual(True,True)

    def test_tfg_tipo(self):
        tfg = Tfg()
        result = tfg_services.insert_tfg(tfg)
        self.assertEqual(True,True)

    def test_tfg_n_alumnos(self):

        tfg = Tfg(n_alumnos=10)
        result = tfg_services.insert_tfg(tfg)
        self.assertEqual(result, False)

    def test_tfg_descripcion(self):
        tfg = Tfg()
        result = tfg_services.insert_tfg(tfg)
        self.assertEqual(True,True)

    def test_tfg_conocimientos_previos(self):
        tfg = Tfg()
        result = tfg_services.insert_tfg(tfg)
        self.assertEqual(True,True)

    def test_tfg_hard_soft(self):
        tfg = Tfg()
        result = tfg_services.insert_tfg(tfg)
        self.assertEqual(True,True)

    def test_tfg_tutor(self):
        tfg = Tfg()
        result = tfg_services.insert_tfg(tfg)
        self.assertEqual(True,True)

    def test_tfg_cotutor(self):
        tfg = Tfg()
        result = tfg_services.insert_tfg(tfg)
        self.assertEqual(True,True)
