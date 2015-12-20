from django.test import TestCase
from django.contrib.auth.models import User, Group
from gestion_tfg.models import Alumno, Profesor
from gestion_tfg.servicios import tfg_services


class TfgServicesTests(TestCase):

    def setUp(self):

        self.presidente = Profesor.objects.create_user(
            username='presidente', email='pepe@ugr.es', password='top_secret', departamento='black mesa')
        self.titular_1 = Profesor.objects.create_user(
            username='titular_1', email='paco@ugr.es', password='top_secret', departamento='black mesa')
        self.titular_2 = Profesor.objects.create_user(
            username='titular_2', email='paco@ugr.es', password='top_secret', departamento='black mesa')
        self.sup_presidente = Profesor.objects.create_user(
            username='sup_presidente', email='paco@ugr.es', password='top_secret', departamento='black mesa')
        self.sup_titular_1 = Profesor.objects.create_user(
            username='sup_titular_1', email='paco@ugr.es', password='top_secret', departamento='black mesa')
        self.sup_titular_2 = Profesor.objects.create_user(
            username='sup_titular_2', email='paco@ugr.es', password='top_secret', departamento='black mesa')

        self.grupo_profesores = Group.objects.get_or_create(name='Profesores')
        self.grupo_alumnos = Group.objects.get_or_create(name='Alumnos')


    def test_formar_comision_error_grupo(self):

        self.presidente.groups.add(self.grupo_profesores[0])
        self.titular_2.groups.add(self.grupo_profesores[0])
        self.sup_titular_1.groups.add(self.grupo_profesores[0])
        self.sup_titular_2.groups.add(self.grupo_profesores[0])

        # suplente del presidente no profesor
        result = tfg_services.formar_comision(presidente=self.presidente, sup_presidente=self.sup_presidente,titular_1= self.titular_1,sup_titular_1= self.sup_titular_1,
                                             titular_2= self.titular_2,sup_titular_2= self.sup_titular_2)
        self.assertEqual(result, False)

        # no primer titular profesor
        self.sup_presidente.groups.add(self.grupo_profesores[0])
        result = tfg_services.formar_comision(presidente=self.presidente, sup_presidente=self.sup_presidente,titular_1= self.titular_1,sup_titular_1= self.sup_titular_1,
                                             titular_2= self.titular_2,sup_titular_2= self.sup_titular_2)
        self.assertEqual(result, False)
        # Valido
        self.titular_1.groups.add(self.grupo_profesores[0])
        result = tfg_services.formar_comision(presidente=self.presidente, sup_presidente=self.sup_presidente,titular_1= self.titular_1,sup_titular_1= self.sup_titular_1,
                                             titular_2= self.titular_2,sup_titular_2= self.sup_titular_2)
        self.assertEqual(result, True)


    def test_formar_comision_error_param(self):

        self.presidente.groups.add(self.grupo_profesores[0])
        self.titular_2.groups.add(self.grupo_profesores[0])
        self.titular_1.groups.add(self.grupo_profesores[0])
        self.sup_titular_1.groups.add(self.grupo_profesores[0])
        self.sup_titular_2.groups.add(self.grupo_profesores[0])
        self.sup_presidente.groups.add(self.grupo_profesores[0])

        # No Presidente
        result = tfg_services.formar_comision(presidente='president_novalido', sup_presidente=self.sup_presidente,titular_1= self.titular_1,sup_titular_1= self.sup_titular_1,
                                             titular_2= self.titular_2,sup_titular_2= self.sup_titular_2)
        self.assertEqual(result, False)

        # No suplente del presidente
        result = tfg_services.formar_comision(presidente='president_novalido', sup_presidente='sin sup presidente' ,titular_1= self.titular_1,sup_titular_1= self.sup_titular_1,
                                             titular_2= self.titular_2,sup_titular_2= self.sup_titular_2)
        self.assertEqual(result, False)

        # No primer titular
        result = tfg_services.formar_comision(presidente=self.presidente, sup_presidente=self.sup_presidente, titular_1='sin suplente', sup_titular_1= self.sup_titular_1,
                                             titular_2= self.titular_2,sup_titular_2= self.sup_titular_2)
        self.assertEqual(result, False)

        # No suplente del primer titular
        result = tfg_services.formar_comision(presidente=self.presidente, sup_presidente=self.sup_presidente,titular_1= self.titular_1,sup_titular_1='sin suplente',
                                             titular_2= self.titular_2,sup_titular_2= self.sup_titular_2)
        self.assertEqual(result, False)

        # No suplente del segundo titular
        result = tfg_services.formar_comision(presidente=self.presidente, sup_presidente=self.sup_presidente, titular_1=self.titular_1,sup_titular_1= self.sup_titular_1,
                                             titular_2= self.titular_2, sup_titular_2='sin suplente')
        self.assertEqual(result, False)

        # No segundo titular y si suplente
        result = tfg_services.formar_comision(presidente=self.presidente, sup_presidente=self.sup_presidente, titular_1=self.titular_1,sup_titular_1= self.sup_titular_1,
                                             titular_2='sin segundo titular', sup_titular_2= self.sup_titular_2)
        self.assertEqual(result, False)

        # Valido
        result = tfg_services.formar_comision(presidente=self.presidente, sup_presidente=self.sup_presidente,titular_1=self.titular_1, sup_titular_1= self.sup_titular_1,
                                             titular_2= self.titular_2, sup_titular_2= self.sup_titular_2)
        self.assertEqual(result, True)

    def test_formar_comision_error_user(self):

        self.presidente.groups.add(self.grupo_profesores[0])
        self.titular_2.groups.add(self.grupo_profesores[0])
        self.titular_1.groups.add(self.grupo_profesores[0])
        self.sup_titular_1.groups.add(self.grupo_profesores[0])
        self.sup_titular_2.groups.add(self.grupo_profesores[0])
        self.sup_presidente.groups.add(self.grupo_profesores[0])

        # Presidente alumno en grupo alumno
        self.new_presidente_false = Alumno.objects.create_user(username='presidente falso', email='pepefalso@ugr.es',
                                                       password='top_secret de mentira')
        self.new_presidente_false.groups.add(self.grupo_alumnos[0])

        result = tfg_services.formar_comision(presidente=self.new_presidente_false, sup_presidente=self.sup_presidente,titular_1= self.titular_1,sup_titular_1= self.sup_titular_1,
                                             titular_2= self.titular_2,sup_titular_2= self.sup_titular_2)
        self.assertEqual(result, False)

        # Presidente alumno en grupo profesor
        self.new_presidente_false.groups.remove(self.grupo_alumnos[0])
        self.new_presidente_false.groups.add(self.grupo_profesores[0])

        result = tfg_services.formar_comision(presidente=self.new_presidente_false, sup_presidente=self.sup_presidente,titular_1= self.titular_1,sup_titular_1= self.sup_titular_1,
                                             titular_2= self.titular_2,sup_titular_2= self.sup_titular_2)
        self.assertEqual(result, False)

        # Valido

        self.new_presidente_true = Profesor.objects.create_user(username='presidente verdadero', email='pepefalso@ugr.es',
                                                       password='top_secret de verdad', departamento= 'uno cualquiera')
        self.new_presidente_true.groups.add(self.grupo_profesores[0])

        result = tfg_services.formar_comision(presidente=self.presidente, sup_presidente=self.sup_presidente,titular_1=self.titular_1, sup_titular_1= self.sup_titular_1,
                                             titular_2= self.titular_2, sup_titular_2= self.sup_titular_2)
        self.assertEqual(result, True)