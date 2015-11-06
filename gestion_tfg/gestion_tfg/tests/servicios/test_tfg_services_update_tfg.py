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

        #titulo correcto
        campos = {}
        campos['titulo'] = self.otro_titulo_tfg

        tfg = Tfg.objects.get(titulo=self.titulo_tfg)

        result = tfg_services.update_tfg(tfg, campos)
        self.assertEqual(result, True)

    def test_update_tfg_tipo(self):

        #tipo erroneo
        campos = {}
        campos['tipo'] = ''

        tfg = Tfg.objects.get(tipo=self.tipo_tfg)

        result = tfg_services.update_tfg(tfg, campos)
        self.assertEqual(result, False)

        #tipo formato erroneo
        campos = {}
        campos['tipo'] = 3

        tfg = Tfg.objects.get(tipo=self.tipo_tfg)

        result = tfg_services.update_tfg(tfg, campos)
        self.assertEqual(result, False)

        #tipo correcto
        campos = {}
        campos['tipo'] = self.otro_tipo_tfg

        tfg = Tfg.objects.get(tipo=self.tipo_tfg)

        result = tfg_services.update_tfg(tfg, campos)
        self.assertEqual(result, True)

    def test_update_tfg_n_alumnos(self):

        #titulo erroneo
        campos = {}
        campos['n_alumnos'] = 0

        tfg = Tfg.objects.get(n_alumnos=self.n_alumnos_tfg)

        result = tfg_services.update_tfg(tfg, campos)
        self.assertEqual(result, False)

        #titulo formato erroneo
        campos = {}
        campos['n_alumnos'] = 'error'

        tfg = Tfg.objects.get(n_alumnos=self.n_alumnos_tfg)

        result = tfg_services.update_tfg(tfg, campos)
        self.assertEqual(result, False)

        #titulo correcto
        campos = {}
        campos['n_alumnos'] = self.otro_n_alumnos_tfg

        tfg = Tfg.objects.get(n_alumnos=self.n_alumnos_tfg)

        result = tfg_services.update_tfg(tfg, campos)
        self.assertEqual(result, True)

    def test_update_tfg_descripcion(self):

        #tipo erroneo
        campos = {}
        campos['descripcion'] = ''

        tfg = Tfg.objects.get(descripcion=self.descripcion_tfg)

        result = tfg_services.update_tfg(tfg, campos)
        self.assertEqual(result, False)

        #tipo formato erroneo
        campos = {}
        campos['descripcion'] = 3

        tfg = Tfg.objects.get(descripcion=self.descripcion_tfg)

        result = tfg_services.update_tfg(tfg, campos)
        self.assertEqual(result, False)

        #tipo correcto
        campos = {}
        campos['descripcion'] = self.otro_descripcion_tfg

        tfg = Tfg.objects.get(descripcion=self.descripcion_tfg)

        result = tfg_services.update_tfg(tfg, campos)
        self.assertEqual(result, True)

    def test_update_tfg_conocimientos_previos(self):

        #tipo erroneo
        campos = {}
        campos['conocimientos_previos'] = ''

        tfg = Tfg.objects.get(conocimientos_previos=self.conocimientos_previos_tfg)

        result = tfg_services.update_tfg(tfg, campos)
        self.assertEqual(result, False)

        #tipo formato erroneo
        campos = {}
        campos['conocimientos_previos'] = 3

        tfg = Tfg.objects.get(conocimientos_previos=self.conocimientos_previos_tfg)

        result = tfg_services.update_tfg(tfg, campos)
        self.assertEqual(result, False)

        #tipo correcto
        campos = {}
        campos['conocimientos_previos'] = self.otro_conocimientos_previos_tfg

        tfg = Tfg.objects.get(conocimientos_previos=self.conocimientos_previos_tfg)

        result = tfg_services.update_tfg(tfg, campos)
        self.assertEqual(result, True)

    def test_update_tfg_hard_soft(self):

        #tipo erroneo
        campos = {}
        campos['hard_soft'] = ''

        tfg = Tfg.objects.get(hard_soft=self.hard_soft_tfg)

        result = tfg_services.update_tfg(tfg, campos)
        self.assertEqual(result, False)

        #tipo formato erroneo
        campos = {}
        campos['hard_soft'] = 3

        tfg = Tfg.objects.get(hard_soft=self.hard_soft_tfg)

        result = tfg_services.update_tfg(tfg, campos)
        self.assertEqual(result, False)

        #tipo correcto
        campos = {}
        campos['hard_soft'] = self.otro_hard_soft_tfg

        tfg = Tfg.objects.get(hard_soft=self.hard_soft_tfg)

        result = tfg_services.update_tfg(tfg, campos)
        self.assertEqual(result, True)

    def test_update_tfg_tutor(self):

        #tipo erroneo
        campos = {}
        campos['tutor'] = ''

        tfg = Tfg.objects.get(tutor=self.user_tutor_tfg)

        result = tfg_services.update_tfg(tfg, campos)
        self.assertEqual(result, False)

        #tipo formato erroneo
        campos = {}
        campos['tutor'] = 3

        tfg = Tfg.objects.get(tutor=self.user_tutor_tfg)

        result = tfg_services.update_tfg(tfg, campos)
        self.assertEqual(result, False)

        #tipo correcto
        campos = {}
        campos['tutor'] = self.otro_user_tutor_tfg

        tfg = Tfg.objects.get(tutor=self.user_tutor_tfg)

        result = tfg_services.update_tfg(tfg, campos)
        self.assertEqual(result, True)

    def test_update_tfg_cotutor(self):

        #tipo erroneo
        campos = {}
        campos['cotutor'] = ''

        tfg = Tfg.objects.get(cotutor=self.user_cotutor_tfg)

        result = tfg_services.update_tfg(tfg, campos)
        self.assertEqual(result, False)

        #tipo formato erroneo
        campos = {}
        campos['cotutor'] = 3

        tfg = Tfg.objects.get(cotutor=self.user_cotutor_tfg)

        result = tfg_services.update_tfg(tfg, campos)
        self.assertEqual(result, False)

        #tipo correcto
        campos = {}
        campos['cotutor'] = self.otro_user_cotutor_tfg

        tfg = Tfg.objects.get(cotutor=self.user_cotutor_tfg)

        result = tfg_services.update_tfg(tfg, campos)
        self.assertEqual(result, True)