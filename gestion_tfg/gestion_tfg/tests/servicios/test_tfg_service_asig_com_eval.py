from django.test import TestCase
from django.contrib.auth.models import User, Group
from gestion_tfg.models import Alumno, Profesor
from gestion_tfg.servicios import tfg_services


class TfgServicesTests(TestCase):

    def setUp(self):

        self.presidente = Profesor.objects.create_user(
            username='presidente', email='pepe@ugr.es', password='top_secret')
        self.titular_1 = Profesor.objects.create_user(
            username='titular_1', email='paco@ugr.es', password='top_secret')
        self.titular_2 = Profesor.objects.create_user(
            username='titular_2', email='paco@ugr.es', password='top_secret')
        self.sup_presidente = Profesor.objects.create_user(
            username='sup_presidente', email='paco@ugr.es', password='top_secret')
        self.sup_titular_1 = Profesor.objects.create_user(
            username='sup_titular_1', email='paco@ugr.es', password='top_secret')
        self.sup_titular_2 = Profesor.objects.create_user(
            username='sup_titular_2', email='paco@ugr.es', password='top_secret')

        self.grupo_profesores = Group.objects.get_or_create(name='Profesores')

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