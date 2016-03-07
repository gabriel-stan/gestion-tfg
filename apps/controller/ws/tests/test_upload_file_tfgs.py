# -*- coding: utf-8 -*-
__author__ = 'tonima'
import simplejson as json
import os
from django.contrib.auth.models import Group
from django.test import TestCase
from model.models import Tfg
from controller.servicios import tfg_services
from rest_framework.test import APIClient


class TfgServicesTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.data_prof1 = dict(username='jorgecasillas@ugr.es', first_name='profesor 1',
                               last_name='apellido 1 apellido 12', departamento='el mas mejor')

        self.data_prof2 = dict(username='juanmanuelfernandez@ugr.es', first_name='profesor 2',
                               last_name='apellido 12 apellido 122', departamento='el mas mejor')

        self.data_prof3 = dict(username='eugenioaguirre@ugr.es', first_name='profesor 2',
                               last_name='apellido 12 apellido 122', departamento='el mas mejor')

        self.data_prof4 = dict(username='miguelgarcia@ugr.es', first_name='profesor 2',
                               last_name='apellido 12 apellido 122', departamento='el mas mejor')

        self.data_prof5 = dict(username='franciscoherrera@ugr.es', first_name='profesor 2',
                               last_name='apellido 12 apellido 122', departamento='el mas mejor')

        self.user_tutor1_tfg = self.client.post('/profesores/', self.data_prof1)
        self.user_tutor2_tfg = self.client.post('/profesores/', self.data_prof2)
        self.user_tutor3_tfg = self.client.post('/profesores/', self.data_prof3)
        self.user_tutor4_tfg = self.client.post('/profesores/', self.data_prof4)
        self.user_tutor5_tfg = self.client.post('/profesores/', self.data_prof5)

        self.data_tfg1 = dict(tipo='tipo1', titulo='titulo1',
                              n_alumnos=2, descripcion='descripcion',
                              conocimientos_previos='conocimientos previos',
                              hard_soft='hard_soft', tutor=self.data_prof1['username'],
                              cotutor=self.data_prof2['username'])

        self.data_tfg2 = dict(tipo='tipo1', titulo='titulo1',
                              n_alumnos=2, descripcion='descripcion',
                              conocimientos_previos='conocimientos previos',
                              hard_soft='hard_soft', tutor=self.data_prof2['username'],
                              cotutor=self.data_prof2['username'])

        self.data_tfg_error = dict(titulo='titulo1',
                                   n_alumnos=2, descripcion='descripcion',
                                   conocimientos_previos='conocimientos previos',
                                   hard_soft='conocimientos previos', tutor=self.user_tutor1_tfg,
                                   cotutor=self.user_tutor2_tfg)

        # TODO: Hacer que carge desde el fichero cases sin que pete el test,
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
        # Envio el fichero y carga TFGs
        location = os.path.join(os.path.dirname(__file__), 'test_upload_file_tfgs', 'ListaTFGs.xlsx')
        data = {'file': ('ListaTFGs.xlsx', open(location, 'rb')), 'filas': 5}
        res = self.client.post('/upload_file_tfgs/', data, format='multipart')
        resul = json.loads(res.content)
        res = self.client.get('/tfgs/', {'titulo': self.TFG1['titulo']})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
