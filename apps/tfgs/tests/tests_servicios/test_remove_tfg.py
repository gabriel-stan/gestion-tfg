from django.contrib.auth.models import Group
from django.test import TestCase

from old.controller.servicios import tfg_services
from model.models import Tfg, Profesor
from gestion_tfgs import servicios


class TfgServicesTests(TestCase):
    def setUp(self):

        self.tipo_tfg = 'tipo1'
        self.titulo_tfg = 'titulo1'
        self.n_alumnos_tfg = 2
        self.descripcion_tfg = 'descripcion'
        self.conocimientos_previos_tfg = 'conocimientos previos'
        self.hard_soft_tfg = 'hardware software'

        self.user_tutor_tfg = tfg_services.insert_profesor(Profesor(username='pepe@ugr.es',
                                                                    first_name='pepe', last_name='paco', departamento='departamento 1'))['data']
        self.user_cotutor_tfg = tfg_services.insert_profesor(Profesor(username='paco@ugr.es',
                                                                      first_name='paco', last_name='pepe', departamento='departamento 2'))['data']

        self.grupo_profesores = Group.objects.get(name='Profesores')
        self.grupo_alumnos = Group.objects.get(name='Alumnos')

        self.grupo_profesores.user_set.add(self.user_tutor_tfg)
        self.grupo_profesores.user_set.add(self.user_cotutor_tfg)

        self.tfg1 = Tfg(tipo=self.tipo_tfg, titulo=self.titulo_tfg,
                   n_alumnos=self.n_alumnos_tfg, descripcion=self.descripcion_tfg,
                   conocimientos_previos=self.conocimientos_previos_tfg,
                   hard_soft=self.hard_soft_tfg, tutor=self.user_tutor_tfg,
                   cotutor=self.user_cotutor_tfg)

        # insertamos un tfg valido
        tfg_services.insert_tfg(self.tfg1)

    def test_delete_tfg_existe(self):

        tfg = Tfg.objects.get(titulo=self.titulo_tfg)
        result = servicios.delete_tfg(tfg)
        self.assertEqual(result['status'], True)
