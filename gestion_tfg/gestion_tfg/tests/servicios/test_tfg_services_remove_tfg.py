from django.test import TestCase
from gestion_tfg.models import Tfg
from django.contrib.auth.models import User, Group

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

        self.grupo_profesores = Group.objects.get_or_create(name='Profesores')
        self.grupo_alumnos = Group.objects.get_or_create(name='Alumnos')

        self.user_tutor_tfg.groups.add(self.grupo_profesores[0])
        self.user_cotutor_tfg.groups.add(self.grupo_profesores[0])

        self.tfg1 = Tfg(tipo=self.tipo_tfg, titulo=self.titulo_tfg,
                   n_alumnos=self.n_alumnos_tfg, descripcion=self.descripcion_tfg,
                   conocimientos_previos=self.conocimientos_previos_tfg,
                   hard_soft=self.hard_soft_tfg, tutor=self.user_tutor_tfg,
                   cotutor=self.user_cotutor_tfg)

        # insertamos un tfg valido
        tfg_services.insert_tfg(self.tfg1)

    def test_delete_tfg_existe(self):

        tfg = Tfg.objects.get(titulo=self.titulo_tfg)
        result = tfg_services.delete_tfg(tfg)
        self.assertEqual(result, False)
