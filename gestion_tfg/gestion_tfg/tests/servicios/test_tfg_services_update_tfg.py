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

        self.otro_tipo_tfg = 'tipo1'
        self.otro_titulo_tfg = 'titulo1'
        self.otro_n_alumnos_tfg = 2
        self.otro_descripcion_tfg = 'descripcion'
        self.otro_conocimientos_previos_tfg = 'conocimientos previos'
        self.otro_hard_soft_tfg = 'hardware software'

        self.otro_user_tutor_tfg = User.objects.create_user(
            username='manuel', email='manuel@ugr.es', password='top_secret')
        self.otro_user_cotutor_tfg = User.objects.create_user(
            username='manolo', email='manolo@ugr.es', password='top_secret')

        self.tfg1 = Tfg(tipo=self.tipo_tfg, titulo=self.titulo_tfg,
                   n_alumnos=self.n_alumnos_tfg, descripcion=self.descripcion_tfg,
                   conocimientos_previos=self.conocimientos_previos_tfg,
                   hard_soft=self.hard_soft_tfg, tutor=self.user_tutor_tfg,
                   cotutor=self.user_cotutor_tfg)

        # insertamos un tfg valido
        tfg_services.insert_tfg(self.tfg1)

    def test_update_tfg_titulo(self):

        #titulo erroneo
        campos = {}
        campos['titulo'] = ''

        tfg = Tfg.objects.get(titulo=self.titulo_tfg)

        result = tfg_services.update_tfg(tfg, campos)
        self.assertEqual(result, False)

        #titulo formato erroneo
        campos = {}
        campos['titulo'] = 3

        tfg = Tfg.objects.get(titulo=self.titulo_tfg)

        result = tfg_services.update_tfg(tfg, campos)
        self.assertEqual(result, False)