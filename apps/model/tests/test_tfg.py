from apps.model.models import Tfg, Profesor
from django.test import TestCase

nuevo_tfg = {}
nuevo_tfg['tipo_tfg'] = 'tipo2'
nuevo_tfg['titulo_tfg'] = 'titulo2'
nuevo_tfg['n_alumnos_tfg'] = 3
nuevo_tfg['descripcion_tfg'] = 'descripcion2'
nuevo_tfg['conocimientos_previos_tfg'] = 'conocimientos muy previos'
nuevo_tfg['hard_soft_tfg'] = 'hardware software nuevo'


class TfgTests(TestCase):

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

    def test_update_tfg(self):

        tfg = Tfg.objects.get(titulo=self.titulo_tfg)
        tfg.tipo = nuevo_tfg['tipo_tfg']
        tfg.titulo = nuevo_tfg['titulo_tfg']
        tfg.n_alumnos = nuevo_tfg['n_alumnos_tfg']
        tfg.descripcion = nuevo_tfg['descripcion_tfg']
        tfg.conocimientos_previos = nuevo_tfg['conocimientos_previos_tfg']
        tfg.hard_soft = nuevo_tfg['hard_soft_tfg']

        tfg.save()

        new_tfg = Tfg.objects.get(titulo=tfg.titulo)

        self.assertEqual(tfg.tipo, new_tfg.tipo)
        self.assertEqual(tfg.titulo, new_tfg.titulo)
        self.assertEqual(tfg.n_alumnos, new_tfg.n_alumnos)
        self.assertEqual(tfg.descripcion, new_tfg.descripcion)
        self.assertEqual(tfg.conocimientos_previos, new_tfg.conocimientos_previos)
        self.assertEqual(tfg.hard_soft, new_tfg.hard_soft)


    def test_delete_tfg(self):

        tfg = Tfg.objects.get(titulo=self.titulo_tfg)
        tfg.delete()

        try:
            tfg = Tfg.objects.get(titulo=self.titulo_tfg)
        except Tfg.DoesNotExist:
            tfg = None

        self.assertEqual(tfg, None)



