__author__ = 'tonima'
from django.test import TestCase
from rest_framework.test import APIClient
from authentication.models import Usuario, Departamento, Profesor
from django.contrib.auth.models import Group
from comisiones_evaluacion.tests.test_upload_file_tfgs.cases import TITULOS
from tfgs.models import Titulacion
import simplejson as json
import os


class ComisionesEvaluacionServicesTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.data_admin = dict(email='admin@admin.es', first_name='admin 1',
                               last_name='apellido 1 apellido 12', password='0000', is_admin=True)
        Usuario.objects.create_superuser(**self.data_admin)

        dep_atc = Departamento.objects.create(nombre='ATC', codigo='ATC')
        dep_lsi = Departamento.objects.create(nombre='LSI', codigo='LSI')
        dep_DECSAI = Departamento.objects.create(nombre='DECSAI', codigo='DECSAI')
        dep_est = Departamento.objects.create(nombre='ESTADISTICA', codigo='ESTADISTICA')

        titulacion = Titulacion.objects.create(nombre='Ingenieria Informatica', codigo='IF')

        self.data_evento1 = dict(content=dict(contenido='admin2@admin.es', convocatoria='CONV_SEPT', tipo='SOL_EVAL',
                                              titulo='titulo 1', desde='2016-08-04T22:00:00.000Z',
                                              hasta='2016-08-14T15:00:00.000Z', titulacion=titulacion.codigo))

        self.data_evento_comision = dict(content=dict(contenido='admin2@admin.es', convocatoria='CONV_SEPT',
                                                      tipo='COM_EVAL', titulo='titulo 1',
                                                      desde='2016-08-15T22:00:00.000Z',
                                                      hasta='2016-08-18T15:00:00.000Z', titulacion=titulacion.codigo))

        self.data_prof1 = dict(email='prof_ejemplo@ugr.es', first_name='profesor 1',
                               last_name='apellido 1 apellido 12', departamento=dep_atc.codigo, password='75169052')

        self.data_prof2 = dict(email='prof_ejemplo2@ugr.es', first_name='profesor 2',
                               last_name='apellido 12 apellido 122', departamento=dep_lsi.codigo, password='75169052')

        self.data_prof3 = dict(email='prof_ejemplo3@ugr.es', first_name='profesor 3',
                               last_name='apellido 12 apellido 122', departamento=dep_DECSAI.codigo, password='75169052')

        self.data_prof4 = dict(email='prof_ejemplo4@ugr.es', first_name='profesor 4',
                               last_name='apellido 12 apellido 122', departamento=dep_est.codigo, password='75169052')

        self.data_tfg1 = dict(tipo='tipo1', titulo='titulo1',
                              n_alumnos=2, descripcion='descripcion',
                              conocimientos_previos='conocimientos previos',
                              hard_soft='hard_soft', tutor=self.data_prof1['email'],
                              cotutor=self.data_prof2['email'], titulacion=titulacion.codigo)

        self.data_alum1 = dict(email='alumno1@correo.ugr.es', first_name='alumno 1',
                               last_name='apellido 12 apellido 122', password='75169052')

        self.grupo_jefe_departamento = Group.objects.get(name='Jefe de Departamento')

        self.prof1 = dict(email='jorgecasillas@ugr.es', first_name='profesor 1', last_name='apellido 1 apellido 12',
                          departamento=dep_atc, password='75169052')
        Profesor.objects.create_user(**self.prof1)
        self.grupo_jefe_departamento.user_set.add(Profesor.objects.get(email='jorgecasillas@ugr.es'))

        self.prof2 = dict(email='juanmanuelfernandez@ugr.es', first_name='profesor 2',
                          last_name='apellido 12 apellido 122', departamento=dep_lsi, password='75169052')
        Profesor.objects.create_user(**self.prof2)

        self.prof3 = dict(email='eugenioaguirre@ugr.es', first_name='profesor 2', last_name='apellido 12 apellido 122',
                          departamento=dep_DECSAI, password='75169052')
        Profesor.objects.create_user(**self.prof3)

        self.prof4 = dict(email='miguelgarcia@ugr.es', first_name='profesor 2', last_name='apellido 12 apellido 122',
                          departamento=dep_est, password='75169052')
        Profesor.objects.create_user(**self.prof4)

        self.prof5 = dict(email='perico@ugr.es', first_name='profesor 2', last_name='apellido 12 apellido 122',
                          departamento=dep_lsi, password='75169052')
        Profesor.objects.create_user(**self.prof5)

        self.prof6 = dict(email='franciscoherrera@ugr.es', first_name='profesor 2', last_name='apellido 12 apellido 122'
                          , departamento=dep_lsi, password='75169052')
        Profesor.objects.create_user(**self.prof6)

        self.prof7 = dict(email='antonio@ugr.es', first_name='profesor 2', last_name='apellido 12 apellido 122',
                          departamento=dep_atc, password='75169052')
        Profesor.objects.create_user(**self.prof7)

        self.prof8 = dict(email='gabriel@ugr.es', first_name='profesor 2', last_name='apellido 12 apellido 122',
                          departamento=dep_DECSAI, password='75169052')
        Profesor.objects.create_user(**self.prof8)

        self.prof9 = dict(email='josemiguel@ugr.es', first_name='profesor 2', last_name='apellido 12 apellido 122',
                          departamento=dep_est, password='75169052')
        Profesor.objects.create_user(**self.prof9)

        self.prof10 = dict(email='qwdefegw@ugr.es', first_name='profesor 2', last_name='apellido 12 apellido 122',
                           departamento=dep_est, password='75169052')
        Profesor.objects.create_user(**self.prof10)

        self.prof11 = dict(email='werwefg@ugr.es', first_name='profesor 2', last_name='apellido 12 apellido 122',
                           departamento=dep_atc, password='75169052')
        Profesor.objects.create_user(**self.prof11)

        self.prof12 = dict(email='qwe123@ugr.es', first_name='qwe123 2', last_name='eq 12 apelliweasdaado 122',
                           departamento=dep_DECSAI, password='7516129052')
        Profesor.objects.create_user(**self.prof12)

        self.prof13 = dict(email='hgm54@ugr.es', first_name='hgm54 2', last_name='dfgre 12 apelergerlido 122',
                           departamento=dep_est, password='751690as52')
        Profesor.objects.create_user(**self.prof13)

        self.prof14 = dict(email='hgm5412@ugr.es', first_name='hgm5412 2', last_name='dfgre 12 apelergerlido 122',
                           departamento=dep_atc, password='751690as52')
        Profesor.objects.create_user(**self.prof14)

        self.prof15 = dict(email='qwe23456fg@ugr.es', first_name='qwe23456fg 2', last_name='dfgrasde 12 apelergewqerlido 122',
                           departamento=dep_DECSAI, password='75121690as52')
        Profesor.objects.create_user(**self.prof15)

        self.prof16 = dict(email='prof16@ugr.es', first_name='prof16 2', last_name='dfgrasde 12 apelergewqerlido 122',
                           departamento=dep_DECSAI, password='75121690as52')
        Profesor.objects.create_user(**self.prof16)

        self.prof17 = dict(email='prof17@ugr.es', first_name='prof17 2', last_name='dfgrasde 12 apelergewqerlido 122',
                           departamento=dep_DECSAI, password='75121690as52')
        Profesor.objects.create_user(**self.prof17)

        self.prof18 = dict(email='prof18@ugr.es', first_name='prof18 2', last_name='dfgrasde 12 apelergewqerlido 122',
                           departamento=dep_DECSAI, password='75121690as52')
        Profesor.objects.create_user(**self.prof18)

        self.prof19 = dict(email='prof19@ugr.es', first_name='prof19 2', last_name='dfgrasde 12 apelergewqerlido 122',
                           departamento=dep_DECSAI, password='75121690as52')
        Profesor.objects.create_user(**self.prof19)

        self.prof20 = dict(email='prof20@ugr.es', first_name='prof20 2', last_name='dfgrasde 12 apelergewqerlido 122',
                           departamento=dep_DECSAI, password='75121690as52')
        Profesor.objects.create_user(**self.prof20)

        self.prof21 = dict(email='prof21@ugr.es', first_name='prof21 2', last_name='dfgrasde 12 apelergewqerlido 122',
                           departamento=dep_DECSAI, password='75121690as52')
        Profesor.objects.create_user(**self.prof21)

    def test_formacion_comisiones(self):
        # Login como administrador
        res = self.client.post('/api/v1/auth/login/', dict(email=self.data_admin['email'],
                                                           password=self.data_admin['password']))

        # Inserto los profesores
        res = self.client.post('/api/v1/profesores/', self.data_prof1)
        resul = json.loads(res.content)
        self.assertEqual(resul['data']['email'], self.data_prof1['email'])

        res = self.client.post('/api/v1/profesores/', self.data_prof2)
        resul = json.loads(res.content)
        self.assertEqual(resul['data']['email'], self.data_prof2['email'])

        res = self.client.post('/api/v1/tfgs/', self.data_tfg1)
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        res = self.client.post('/api/v1/alumnos/', self.data_alum1)

        # Asigno el TFG
        res = self.client.post('/api/v1/tfgs_asig/', {'tfg': self.data_tfg1['titulo'],
                                                      'alumno_1': self.data_alum1['email']})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Creo la convocatoria de Septiembre
        res = self.client.post('/api/v1/events/',  self.data_evento1, format='json')
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Creo la convocatoria para la formacion de la comisiones
        res = self.client.post('/api/v1/events/',  self.data_evento_comision, format='json')
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Le asigno una convocatoria
        res = self.client.put('/api/v1/tfgs_asig/', {'tfg': self.data_tfg1['titulo'], 'datos': json.dumps(
            {'convocatoria': 'CONV_SEPT', 'anio': 2016})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Envio el fichero y carga TFGs
        location = os.path.join(os.path.dirname(__file__), 'test_upload_file_tfgs', 'ListaTFGs_preasignados.xlsx')
        data = {'file': ('ListaTFGs_preasignados.xlsx', open(location, 'rb')), 'u_fila': 24, 'p_fila': 5,
                'cabeceras': json.dumps(dict(tipo='D', titulo='E', n_alumnos='F', alumno_1='G', alumno_2='H',
                                             descripcion='I', conocimientos_previos='J', hard_soft='K', tutor='B',
                                             cotutor='C', titulacion='L')), 'type_file': 'tfg_asig',
                'titulacion': 'IF'}
        res = self.client.post('/api/v1/upload_file_tfgs/', data, format='multipart')
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        res = self.client.post('/api/v1/upload_file_tfgs_confirm/', data={'list_tfg': json.dumps(resul['exitos']),
                                                                          'model': 'tfg_asig'})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Envio el fichero y carga de otros TFGs
        location = os.path.join(os.path.dirname(__file__), 'test_upload_file_tfgs', 'ListaTFGs_preasignados_otros.xlsx')
        data = {'file': ('ListaTFGs_preasignados_otros.xlsx', open(location, 'rb')), 'u_fila': 10, 'p_fila': 5,
                'cabeceras': json.dumps(dict(tipo='D', titulo='E', n_alumnos='F', alumno_1='G', alumno_2='H',
                                             descripcion='I', conocimientos_previos='J', hard_soft='K', tutor='B',
                                             cotutor='C', titulacion='L')), 'type_file': 'tfg_asig',
                'titulacion': 'GII'}
        res = self.client.post('/api/v1/upload_file_tfgs/', data, format='multipart')
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        res = self.client.post('/api/v1/upload_file_tfgs_confirm/', data={'list_tfg': json.dumps(resul['exitos']),
                                                                          'model': 'tfg_asig'})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Le asigno una convocatoria
        res = self.client.put('/api/v1/tfgs_asig/', {'tfg': TITULOS[0], 'datos': json.dumps(
            {'convocatoria': 'CONV_SEPT', 'anio': 2016})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Le asigno una convocatoria
        res = self.client.put('/api/v1/tfgs_asig/', {'tfg': TITULOS[1], 'datos': json.dumps(
            {'convocatoria': 'CONV_SEPT', 'anio': 2016})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Le asigno una convocatoria
        res = self.client.put('/api/v1/tfgs_asig/', {'tfg': TITULOS[2], 'datos': json.dumps(
            {'convocatoria': 'CONV_SEPT', 'anio': 2016})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Le asigno una convocatoria
        res = self.client.put('/api/v1/tfgs_asig/', {'tfg': TITULOS[3], 'datos': json.dumps(
            {'convocatoria': 'CONV_SEPT', 'anio': 2016})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Le asigno una convocatoria
        res = self.client.put('/api/v1/tfgs_asig/', {'tfg': TITULOS[4], 'datos': json.dumps(
            {'convocatoria': 'CONV_SEPT', 'anio': 2016})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Le asigno una convocatoria
        res = self.client.put('/api/v1/tfgs_asig/', {'tfg': TITULOS[5], 'datos': json.dumps(
            {'convocatoria': 'CONV_SEPT', 'anio': 2016})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Le asigno una convocatoria
        res = self.client.put('/api/v1/tfgs_asig/', {'tfg': TITULOS[6], 'datos': json.dumps(
            {'convocatoria': 'CONV_SEPT', 'anio': 2016})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Le asigno una convocatoria
        res = self.client.put('/api/v1/tfgs_asig/', {'tfg': TITULOS[7], 'datos': json.dumps(
            {'convocatoria': 'CONV_SEPT', 'anio': 2016})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Le asigno una convocatoria
        res = self.client.put('/api/v1/tfgs_asig/', {'tfg': TITULOS[8], 'datos': json.dumps(
            {'convocatoria': 'CONV_SEPT', 'anio': 2016})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Le asigno una convocatoria
        res = self.client.put('/api/v1/tfgs_asig/', {'tfg': TITULOS[9], 'datos': json.dumps(
            {'convocatoria': 'CONV_SEPT', 'anio': 2016})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Le asigno una convocatoria
        res = self.client.put('/api/v1/tfgs_asig/', {'tfg': TITULOS[10], 'datos': json.dumps(
            {'convocatoria': 'CONV_SEPT', 'anio': 2016})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Le asigno una convocatoria
        res = self.client.put('/api/v1/tfgs_asig/', {'tfg': TITULOS[11], 'datos': json.dumps(
            {'convocatoria': 'CONV_SEPT', 'anio': 2016})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Le asigno una convocatoria
        res = self.client.put('/api/v1/tfgs_asig/', {'tfg': TITULOS[12], 'datos': json.dumps(
            {'convocatoria': 'CONV_SEPT', 'anio': 2016})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Le asigno una convocatoria
        res = self.client.put('/api/v1/tfgs_asig/', {'tfg': TITULOS[13], 'datos': json.dumps(
            {'convocatoria': 'CONV_SEPT', 'anio': 2016})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Le asigno una convocatoria
        res = self.client.put('/api/v1/tfgs_asig/', {'tfg': TITULOS[14], 'datos': json.dumps(
            {'convocatoria': 'CONV_SEPT', 'anio': 2016})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Le asigno una convocatoria
        res = self.client.put('/api/v1/tfgs_asig/', {'tfg': TITULOS[15], 'datos': json.dumps(
            {'convocatoria': 'CONV_SEPT', 'anio': 2016})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Le asigno una convocatoria
        res = self.client.put('/api/v1/tfgs_asig/', {'tfg': TITULOS[16], 'datos': json.dumps(
            {'convocatoria': 'CONV_SEPT', 'anio': 2016})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Le asigno una convocatoria
        res = self.client.put('/api/v1/tfgs_asig/', {'tfg': TITULOS[17], 'datos': json.dumps(
            {'convocatoria': 'CONV_SEPT', 'anio': 2016})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Le asigno una convocatoria
        res = self.client.put('/api/v1/tfgs_asig/', {'tfg': TITULOS[18], 'datos': json.dumps(
            {'convocatoria': 'CONV_SEPT', 'anio': 2016})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Le asigno una convocatoria
        res = self.client.put('/api/v1/tfgs_asig/', {'tfg': TITULOS[19], 'datos': json.dumps(
            {'convocatoria': 'CONV_SEPT', 'anio': 2016})})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

        # Creo una comision
        res = self.client.post('/api/v1/comisiones/', {'convocatoria': 'CONV_SEPT', 'anio': 2016, 'titulacion': 'IF'})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        self.assertEqual(len(resul['data']['tribunales']), 4)

        # Modifico la comision
        destino = resul['data']['tribunales'][1]['presidente']['email']
        res = self.client.put('/api/v1/comisiones/', {'presidente': resul['data']['tribunales'][0]['presidente']['email'],
                                                      'datos': json.dumps({'presidente': destino})})
        resul = json.loads(res.content)
        self.assertEqual(resul['data']['presidente']['email'], destino)

        # Creo los tribunales
        res = self.client.post('/api/v1/tribunales/', {'comisiones': True, 'convocatoria': 'CONV_SEPT', 'anio': 2016,
                                                       'titulacion': 'IF'})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        self.assertEqual(len(resul['data']['tribunales'][0]['tfgs']), 6)

        # Obtengo los tribunales
        res = self.client.get('/api/v1/tribunales/')
        resul = json.loads(res.content)
        self.assertEqual(len(resul['data']), 21)

        # Modifico la fecha de uno
        res = self.client.put('/api/v1/tribunales/', {'tfg': resul['data'][0]['tfg']['tfg']['titulo'],
                                                      'datos': json.dumps({'fecha': '2016-07-04T22:00:00.000Z'})})
        resul = json.loads(res.content)
        self.assertEqual(resul['data']['fecha'], '2016-07-04T22:00:00Z')

        # Obtengo los tribunales
        res = self.client.get('/api/v1/tribunales/')
        resul = json.loads(res.content)
        self.assertEqual(len(resul['data']), 21)

        # Modifico la documentacion de otro
        location = os.path.join(os.path.dirname(__file__), 'test_upload_file_tfgs', 'asd.zip')
        res = self.client.post('/api/v1/upload_doc/', data={'tfg': resul['data'][0]['tfg']['tfg']['titulo'],
                                                            'file': ('ListaTFGs_preasignados.xlsx',
                                                                     open(location, 'rb'))},
                               format='multipart')
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

