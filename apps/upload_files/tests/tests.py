# -*- coding: utf-8 -*-
__author__ = 'tonima'
import os
import simplejson as json
from django.contrib.auth.models import Group
from django.test import TestCase
from rest_framework.test import APIClient
from authentication.models import Profesor, Usuario, Departamento, Alumno
from tfgs.models import Titulacion


class TfgServicesTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.grupo_jefe_departamento = Group.objects.get(name='Jefe de Departamento')

        self.data_admin = dict(email='admin@admin.es', first_name='admin 1',
                               last_name='apellido 1 apellido 12', password='0000', is_admin=True)
        Usuario.objects.create_superuser(**self.data_admin)

        dep = Departamento.objects.create(nombre='departamento1', codigo=1)

        titulacion = Titulacion.objects.create(nombre='Ingenieria Informatica', codigo='GII')

        self.prof1 = dict(email='jorgecasillas@ugr.es', first_name='profesor 1', last_name='apellido 1 apellido 12',
                          departamento=dep, password='75169052')
        Profesor.objects.create_user(**self.prof1)
        self.grupo_jefe_departamento.user_set.add(Profesor.objects.get(email='jorgecasillas@ugr.es'))

        self.prof2 = dict(email='juanmanuelfernandez@ugr.es', first_name='profesor 2',
                          last_name='apellido 12 apellido 122', departamento=dep, password='75169052')
        Profesor.objects.create_user(**self.prof2)

        self.prof3 = dict(email='eugenioaguirre@ugr.es', first_name='profesor 2', last_name='apellido 12 apellido 122',
                          departamento=dep, password='75169052')
        Profesor.objects.create_user(**self.prof3)

        self.prof4 = dict(email='miguelgarcia@ugr.es', first_name='profesor 2', last_name='apellido 12 apellido 122',
                          departamento=dep, password='75169052')
        Profesor.objects.create_user(**self.prof4)

        self.prof5 = dict(email='franciscoherrera@ugr.es', first_name='profesor 2', last_name='apellido 12 apellido 122'
                          , departamento=dep, password='75169052')
        Profesor.objects.create_user(**self.prof5)

        self.data_tfg1 = dict(tipo='tipo1', titulo='titulo1',
                              n_alumnos=2, descripcion='descripcion',
                              conocimientos_previos='conocimientos previos',
                              hard_soft='hard_soft', tutor=self.prof1,
                              cotutor=self.prof2, titulacion=titulacion.codigo)

        self.data_tfg2 = dict(tipo='tipo1', titulo='titulo1',
                              n_alumnos=2, descripcion='descripcion',
                              conocimientos_previos='conocimientos previos',
                              hard_soft='hard_soft', tutor=self.prof1,
                              cotutor=self.prof2, titulacion=titulacion.codigo)

        self.data_tfg_error = dict(titulo='titulo1',
                                   n_alumnos=2, descripcion='descripcion',
                                   conocimientos_previos='conocimientos previos',
                                   hard_soft='conocimientos previos', tutor=self.prof1,
                                   cotutor=self.prof2, titulacion=titulacion.codigo)

        self.TFG1 = {'tipo': 'T2',
                     'titulo': 'Análisis Exploratorio de Datos Mediante Técnicas de Visualización Avanzada',
                     'n_alumnos': '1',
                     'descripcion': 'Vivimos en la era de la información y la transparencia. Nos rodea una inmensidad de datos que '
                                    'dificilmente podemos abordar con las técnicas clásisas de análisis de datos y aprendizaje. '
                                    'Existen numerosas fuentes públicas (por ejemplo, http://www.ine.es, http://www.dgt.es, '
                                    'http://ers.usda.gov, http://badc.nerc.ac.uk, http://www.edenextdata.com) que ofrecen datos '
                                    'interesantísimos sobre aspectos cruciales para la sociedad actual tales como educación, '
                                    'sanidad, igualdad, migración, economía, etc. Sin embargo, quedan en eso, en gran cantidad de '
                                    'datos difíciles de procesar, estudiar, analizar, relacionar o contextualizar. Se trata además '
                                    'de datos poco estructurados y sin relaciones de causalidad que permitan abordar el tradicional'
                                    ' enfoque predictivo. Por todo ello, con el desarrollo de la tecnología y el software, cada vez '
                                    'está cobrando más interés el análisis exploratorio de estos datos empleando recursos gráficos '
                                    'y visuales impactantes y esclarecedores. Aquí encontramos algunos ejemplos prácticos '
                                    'relacionados con el periodismo de datos: http://www.theguardian.com/data, '
                                    'http://www.tableausoftware.com/public/community/viz-of-the-day, '
                                    'http://granadaendatos.granadaimedia.com/. El proyecto abordará ente novedoso enfoque de '
                                    'análisis de datos mediante la selección de casos de especial interés y actualidad, '
                                    'recuperación de datos, manipulación y tratamiento, y su exploración mediante software '
                                    'específico tal como Tableau Software, TIBCO Spotfire o R así como numerosas bibliotecas '
                                    'de JavaScript.',
                     'conocimientos_previos': 'Ninguno.',
                     'hard_soft': 'Ninguno.',
                     'tutor': 'jorgecasillas@ugr.es'}

    def test_ws_upload_file_tfgs(self):
        # Me logueo con un admin
        res = self.client.post('/api/v1/auth/login/', {'email': self.data_admin['email'],
                                                       'password': self.data_admin['password']})
        resul = json.loads(res.content)
        self.assertEqual(resul['data']['email'], self.data_admin['email'])

        # Envio el fichero y carga TFGs
        location = os.path.join(os.path.dirname(__file__), 'test_upload_file_tfgs', 'ListaTFGs.xlsx')
        data = {'file': ('ListaTFGs.xlsx', open(location, 'rb')), 'u_fila': 9, 'p_fila': 5,
                'cabeceras': json.dumps(dict(tipo='D', titulo='E', n_alumnos='F', descripcion='G',
                                             conocimientos_previos='H', hard_soft='I', tutor='B', cotutor='C',
                                             titulacion='J')), 'type_file': 'tfg', 'titulacion': 'GII'}
        res = self.client.post('/api/v1/upload_file_tfgs/', data, format='multipart')
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        self.assertEqual(resul['errores'][1]['fila'], 8)
        self.assertEqual(resul['errores'][1]['message'], 'El TFG no tiene titulo')
        self.assertEqual(resul['errores'][0]['fila'], 6)
        self.assertEqual(resul['errores'][0]['message'], 'El profesor no existe')
        res = self.client.post('/api/v1/upload_file_tfgs_confirm/', data={'list_tfg': json.dumps(resul['exitos']),
                                                                          'model': 'tfg'})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        self.assertEqual(resul['errores'], [])
        res = self.client.post('/api/v1/auth/login/', {'email':'jorgecasillas@ugr.es', 'password':'75169052'})
        resul = json.loads(res.content)
        self.assertEqual(resul['data']['email'], 'jorgecasillas@ugr.es')
        # res = self.client.get('/api/v1/tfgs/', {'titulo': self.TFG1['titulo']})
        # resul = json.loads(res.content)
        # self.assertEqual(resul['data']['tutor']['email'], 'jorgecasillas@ugr.es')

    def test_ws_upload_file_tfgs_preasignados(self):
        # Me logueo con un admin
        res = self.client.post('/api/v1/auth/login/', {'email': self.data_admin['email'],
                                                       'password': self.data_admin['password']})
        resul = json.loads(res.content)
        self.assertEqual(resul['data']['email'], self.data_admin['email'])

        # Envio el fichero y carga TFGs
        location = os.path.join(os.path.dirname(__file__), 'test_upload_file_tfgs', 'ListaTFGs_preasignados.xlsx')
        data = {'file': ('ListaTFGs_preasignados.xlsx', open(location, 'rb')), 'u_fila': 9, 'p_fila': 5,
                'cabeceras': json.dumps(dict(tipo='D', titulo='E', n_alumnos='F', alumno_1='G', alumno_2='H',
                                             descripcion='I', conocimientos_previos='J', hard_soft='K', tutor='B',
                                             cotutor='C', titulacion='L')), 'type_file': 'tfg_asig',
                'titulacion': 'GII'}
        res = self.client.post('/api/v1/upload_file_tfgs/', data, format='multipart')
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        self.assertEqual(resul['exitos'][0]['fila'], 5)
        self.assertEqual(resul['exitos'][0]['tfg']['alumno_1'], 'tonima@correo.ugr.es')
        res = self.client.post('/api/v1/upload_file_tfgs_confirm/', data={'list_tfg': json.dumps(resul['exitos']),
                                                                          'model': 'tfg_asig'})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        res = self.client.post('/api/v1/auth/login/', {'email':'admin@admin.es', 'password':'0000'})
        resul = json.loads(res.content)
        self.assertEqual(resul['data']['email'], 'admin@admin.es')
        res = self.client.get('/api/v1/usuarios/', {'email': 'tonima@correo.ugr.es'})
        resul = json.loads(res.content)
        self.assertEqual(resul['data'][0]['email'], 'tonima@correo.ugr.es')
