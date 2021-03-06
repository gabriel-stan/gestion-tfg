from django.contrib.auth.models import Group
from django.test import TestCase

from old.controller.servicios import tfg_services
from model.models import Alumno, Profesor


class TfgServicesTests(TestCase):

    def setUp(self):
        self.presidente = tfg_services.insert_profesor(Profesor(username='pepe@ugr.es',
                                                                first_name='presidente', last_name='pepe',
                                                                departamento='black mesa4'))['data']
        self.titular_1 = tfg_services.insert_profesor(Profesor(username='titular_1@ugr.es',
                                                               first_name='titular_1', last_name='paco',
                                                               departamento='black mesa3'))['data']
        self.titular_2 = tfg_services.insert_profesor(Profesor(username='paco@ugr.es',
                                                               first_name='titular_2', last_name='pepe',
                                                               departamento='black mesa1'))['data']
        self.sup_presidente = tfg_services.insert_profesor(Profesor(username='sup_presidente@ugr.es',
                                                                    first_name='sup_presidente', last_name='pepe',
                                                                    departamento='black mesa3'))['data']
        self.sup_titular_1 = tfg_services.insert_profesor(Profesor(username='manuel3@ugr.es',
                                                                   first_name='sup_titular_1', last_name='manuel',
                                                                   departamento='black mesa2'))['data']
        self.sup_titular_2 = tfg_services.insert_profesor(Profesor(username='manolo@ugr.es',
                                                                   first_name='sup_titular_2', last_name='pepe',
                                                                   departamento='black mesa2'))['data']

        self.user_alumn1_tfg = tfg_services.insert_alumno(Alumno(username='alumn1@correo.ugr.es', first_name='alumn1',
                                                                 last_name='apellidos 1'))['data']

        self.grupo_profesores = Group.objects.get_or_create(name='Profesores')
        self.grupo_alumnos = Group.objects.get_or_create(name='Alumnos')

    def test_formar_comision_error_grupo(self):

        self.presidente.groups.add(self.grupo_profesores[0])
        self.titular_2.groups.add(self.grupo_profesores[0])
        self.sup_titular_1.groups.add(self.grupo_profesores[0])
        self.sup_titular_2.groups.add(self.grupo_profesores[0])

        # suplente del presidente no profesor
        result = tfg_services.formar_comision(presidente=self.presidente, sup_presidente=self.user_alumn1_tfg,
                                              titular_1=self.titular_1, sup_titular_1=self.sup_titular_1,
                                              titular_2=self.titular_2, sup_titular_2=self.sup_titular_2)
        self.assertEqual(result['status'], False)

        # no primer titular profesor
        self.sup_presidente.groups.add(self.grupo_profesores[0])
        result = tfg_services.formar_comision(presidente=self.presidente, sup_presidente=self.sup_presidente,
                                              titular_1=self.user_alumn1_tfg, sup_titular_1=self.sup_titular_1,
                                              titular_2=self.titular_2, sup_titular_2=self.sup_titular_2)
        self.assertEqual(result['status'], False)
        # Valido
        self.titular_1.groups.add(self.grupo_profesores[0])
        result = tfg_services.formar_comision(presidente=self.presidente, sup_presidente=self.sup_presidente,
                                              titular_1=self.titular_1, sup_titular_1=self.sup_titular_1,
                                              titular_2=self.titular_2, sup_titular_2=self.sup_titular_2)
        self.assertEqual(result['status'], True)

    def test_formar_comision_error_param(self):

        self.presidente.groups.add(self.grupo_profesores[0])
        self.titular_2.groups.add(self.grupo_profesores[0])
        self.titular_1.groups.add(self.grupo_profesores[0])
        self.sup_titular_1.groups.add(self.grupo_profesores[0])
        self.sup_titular_2.groups.add(self.grupo_profesores[0])
        self.sup_presidente.groups.add(self.grupo_profesores[0])

        # No Presidente
        result = tfg_services.formar_comision(presidente='president_novalido', sup_presidente=self.sup_presidente,
                                              titular_1=self.titular_1, sup_titular_1=self.sup_titular_1,
                                              titular_2=self.titular_2, sup_titular_2=self.sup_titular_2)
        self.assertEqual(result['status'], False)

        # No suplente del presidente
        result = tfg_services.formar_comision(presidente='president_novalido', sup_presidente='sin sup presidente',
                                              titular_1=self.titular_1, sup_titular_1=self.sup_titular_1,
                                              titular_2=self.titular_2, sup_titular_2=self.sup_titular_2)
        self.assertEqual(result['status'], False)

        # No primer titular
        result = tfg_services.formar_comision(presidente=self.presidente, sup_presidente=self.sup_presidente,
                                              titular_1='sin suplente', sup_titular_1=self.sup_titular_1,
                                              titular_2=self.titular_2, sup_titular_2=self.sup_titular_2)
        self.assertEqual(result['status'], False)

        # No suplente del primer titular
        result = tfg_services.formar_comision(presidente=self.presidente, sup_presidente=self.sup_presidente,
                                              titular_1=self.titular_1, sup_titular_1='sin suplente',
                                              titular_2=self.titular_2, sup_titular_2=self.sup_titular_2)
        self.assertEqual(result['status'], False)

        # No suplente del segundo titular
        result = tfg_services.formar_comision(presidente=self.presidente, sup_presidente=self.sup_presidente,
                                              titular_1=self.titular_1, sup_titular_1=self.sup_titular_1,
                                              titular_2=self.titular_2, sup_titular_2='sin suplente')
        self.assertEqual(result['status'], False)

        # No segundo titular y si suplente
        result = tfg_services.formar_comision(presidente=self.presidente, sup_presidente=self.sup_presidente,
                                              titular_1=self.titular_1, sup_titular_1=self.sup_titular_1,
                                              titular_2='sin segundo titular', sup_titular_2=self.sup_titular_2)
        self.assertEqual(result['status'], False)

        # Valido
        result = tfg_services.formar_comision(presidente=self.presidente, sup_presidente=self.sup_presidente,
                                              titular_1=self.titular_1, sup_titular_1=self.sup_titular_1,
                                              titular_2=self.titular_2, sup_titular_2=self.sup_titular_2)
        self.assertEqual(result['status'], True)

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

        result = tfg_services.formar_comision(presidente=self.new_presidente_false, sup_presidente=self.sup_presidente,
                                              titular_1=self.titular_1, sup_titular_1=self.sup_titular_1,
                                              titular_2=self.titular_2, sup_titular_2=self.sup_titular_2)
        self.assertEqual(result['status'], False)

        # Presidente alumno en grupo profesor
        self.new_presidente_false.groups.remove(self.grupo_alumnos[0])
        self.new_presidente_false.groups.add(self.grupo_profesores[0])

        result = tfg_services.formar_comision(presidente=self.new_presidente_false, sup_presidente=self.sup_presidente,
                                              titular_1=self.titular_1, sup_titular_1=self.sup_titular_1,
                                              titular_2=self.titular_2, sup_titular_2=self.sup_titular_2)
        self.assertEqual(result['status'], False)

        # Valido

        self.new_presidente_true = Profesor.objects.create_user(username='presidente verdadero',
                                                                email='pepefalso@ugr.es',
                                                                password='top_secret de verdad',
                                                                departamento='uno cualquiera')
        self.new_presidente_true.groups.add(self.grupo_profesores[0])

        result = tfg_services.formar_comision(presidente=self.presidente, sup_presidente=self.sup_presidente,
                                              titular_1=self.titular_1, sup_titular_1=self.sup_titular_1,
                                              titular_2=self.titular_2, sup_titular_2=self.sup_titular_2)
        self.assertEqual(result['status'], True)
