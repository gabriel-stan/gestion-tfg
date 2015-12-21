from django.test import TestCase
from gestion_tfg.models import Tfg, Tfg_Asig, Profesor, Alumno
from django.contrib.auth.models import User

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

        self.tfg = Tfg.objects.create(tipo=self.tipo_tfg, titulo=self.titulo_tfg,
                           n_alumnos=self.n_alumnos_tfg, descripcion=self.descripcion_tfg,
                           conocimientos_previos=self.conocimientos_previos_tfg,
                           hard_soft=self.hard_soft_tfg, tutor=self.user_tutor_tfg,
                           cotutor=self.user_cotutor_tfg)

        self.user_alumn1_tfg = Alumno.objects.create_user(
            username='alumn1', email='alumn1@ugr.es', password='top_secretalumn1')
        self.user_alumn2_tfg = Alumno.objects.create_user(
            username='alumn2', email='alumn2@ugr.es', password='top_secretalumn2')
        self.user_alumn3_tfg = Alumno.objects.create_user(
            username='alumn3', email='alumn3@ugr.es', password='top_secretalumn3')

        self.tfg_asig = Tfg_Asig.objects.create(tfg=self.tfg, alumno_1=self.user_alumn1_tfg, alumno_2=self.user_alumn2_tfg, alumno_3=self.user_alumn3_tfg)

    def test_asig_tfg(self):

        tfg_asig = Tfg_Asig.objects.get(tfg=self.tfg)
        self.assertNotEqual(tfg_asig, None)

    def test_check_tfg_asig(self):

        tfg_asig = Tfg_Asig.objects.get(tfg=self.tfg)

        self.assertEqual(tfg_asig.tfg.tipo, self.tipo_tfg)
        self.assertEqual(tfg_asig.tfg.titulo, self.titulo_tfg)
        self.assertEqual(tfg_asig.tfg.n_alumnos, self.n_alumnos_tfg)
        self.assertEqual(tfg_asig.tfg.descripcion, self.descripcion_tfg)
        self.assertEqual(tfg_asig.tfg.conocimientos_previos, self.conocimientos_previos_tfg)
        self.assertEqual(tfg_asig.tfg.hard_soft, self.hard_soft_tfg)
        self.assertEqual(tfg_asig.tfg.tutor, self.user_tutor_tfg)
        self.assertEqual(tfg_asig.tfg.cotutor, self.user_cotutor_tfg)
        self.assertEqual(tfg_asig.alumno_1, self.user_alumn1_tfg)
        self.assertEqual(tfg_asig.alumno_2, self.user_alumn2_tfg)
        self.assertEqual(tfg_asig.alumno_3, self.user_alumn3_tfg)

    def test_update_tfg_asig(self):

        tfg_asig = Tfg_Asig.objects.get(tfg=self.tfg)
        tfg_asig.tfg.tipo = nuevo_tfg['tipo_tfg']
        tfg_asig.tfg.titulo = nuevo_tfg['titulo_tfg']
        tfg_asig.tfg.n_alumnos = nuevo_tfg['n_alumnos_tfg']
        tfg_asig.tfg.descripcion = nuevo_tfg['descripcion_tfg']
        tfg_asig.tfg.conocimientos_previos = nuevo_tfg['conocimientos_previos_tfg']
        tfg_asig.tfg.hard_soft = nuevo_tfg['hard_soft_tfg']

        tfg_asig.alumno_1 = self.user_alumn2_tfg
        tfg_asig.alumno_2 = self.user_alumn3_tfg
        tfg_asig.alumno_3 = self.user_alumn1_tfg

        tfg_asig.tfg.save()
        tfg_asig.save()

        new_tfg_asig = Tfg_Asig.objects.get(tfg=tfg_asig.tfg)

        self.assertEqual(tfg_asig.tfg.tipo, new_tfg_asig.tfg.tipo)
        self.assertEqual(tfg_asig.tfg.titulo, new_tfg_asig.tfg.titulo)
        self.assertEqual(tfg_asig.tfg.n_alumnos, new_tfg_asig.tfg.n_alumnos)
        self.assertEqual(tfg_asig.tfg.descripcion, new_tfg_asig.tfg.descripcion)
        self.assertEqual(tfg_asig.tfg.conocimientos_previos, new_tfg_asig.tfg.conocimientos_previos)
        self.assertEqual(tfg_asig.tfg.hard_soft, new_tfg_asig.tfg.hard_soft)
        self.assertEqual(tfg_asig.alumno_1, self.user_alumn2_tfg)
        self.assertEqual(tfg_asig.alumno_2, self.user_alumn3_tfg)
        self.assertEqual(tfg_asig.alumno_3, self.user_alumn1_tfg)


    def test_delete_tfg(self):

        tfg_asig = Tfg_Asig.objects.get(tfg=self.tfg)
        tfg_asig.delete()

        try:
            tfg_asig = Tfg_Asig.objects.get(tfg=self.tfg)
        except Tfg_Asig.DoesNotExist:
            tfg_asig = None

        self.assertEqual(tfg_asig, None)



