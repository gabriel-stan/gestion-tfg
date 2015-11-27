from django.test import TestCase
from gestion_tfg.models import Tfg
from django.contrib.auth.models import User

class TfgTests(TestCase):

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

        Tfg.objects.create(tipo=self.tipo_tfg, titulo=self.titulo_tfg,
                           n_alumnos=self.n_alumnos_tfg, descripcion=self.descripcion_tfg,
                           conocimientos_previos=self.conocimientos_previos_tfg,
                           hard_soft=self.hard_soft_tfg, tutor=self.user_tutor_tfg,
                           cotutor=self.user_cotutor_tfg)

    def test_create_tfg(self):

        tfg = Tfg.objects.get(titulo=self.titulo_tfg)
        self.assertNotEqual(tfg, None)

    def test_check_tfg(self):

        tfg = Tfg.objects.get(titulo=self.titulo_tfg)

        self.assertEqual(tfg.tipo, self.tipo_tfg)
        self.assertEqual(tfg.titulo, self.titulo_tfg)
        self.assertEqual(tfg.n_alumnos, self.n_alumnos_tfg)
        self.assertEqual(tfg.descripcion, self.descripcion_tfg)
        self.assertEqual(tfg.conocimientos_previos, self.conocimientos_previos_tfg)
        self.assertEqual(tfg.hard_soft, self.hard_soft_tfg)
        self.assertEqual(tfg.tutor, self.user_tutor_tfg)
        self.assertEqual(tfg.cotutor, self.user_cotutor_tfg)
