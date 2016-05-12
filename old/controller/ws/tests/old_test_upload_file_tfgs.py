# -*- coding: utf-8 -*-
__author__ = 'tonima'
import os

import simplejson as json
from django.contrib.auth.models import Group
from django.test import TestCase
from rest_framework.test import APIClient

from model.models import Profesor


class TfgServicesTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.grupo_profesores = Group.objects.get(name='Profesores')

        self.prof1 = Profesor(username='jorgecasillas@ugr.es', first_name='profesor 1',
                               last_name='apellido 1 apellido 12', departamento='el mas mejor', password='75169052')
        self.prof2 = Profesor(username='juanmanuelfernandez@ugr.es', first_name='profesor 2',
                               last_name='apellido 12 apellido 122', departamento='el mas mejor', password='75169052')
        self.prof3 = Profesor(username='eugenioaguirre@ugr.es', first_name='profesor 2',
                               last_name='apellido 12 apellido 122', departamento='el mas mejor', password='75169052')
        self.prof4 = Profesor(username='miguelgarcia@ugr.es', first_name='profesor 2',
                               last_name='apellido 12 apellido 122', departamento='el mas mejor', password='75169052')
        self.prof5 = Profesor(username='franciscoherrera@ugr.es', first_name='profesor 2',
                               last_name='apellido 12 apellido 122', departamento='el mas mejor', password='75169052')

        self.prof1.save()
        self.prof2.save()
        self.prof3.save()
        self.prof4.save()
        self.prof5.save()

        self.grupo_profesores.user_set.add(self.prof1)
        self.grupo_profesores.user_set.add(self.prof2)
        self.grupo_profesores.user_set.add(self.prof3)
        self.grupo_profesores.user_set.add(self.prof4)
        self.grupo_profesores.user_set.add(self.prof5)

        self.data_tfg1 = dict(tipo='tipo1', titulo='titulo1',
                              n_alumnos=2, descripcion='descripcion',
                              conocimientos_previos='conocimientos previos',
                              hard_soft='hard_soft', tutor=self.prof1,
                              cotutor=self.prof2)

        self.data_tfg2 = dict(tipo='tipo1', titulo='titulo1',
                              n_alumnos=2, descripcion='descripcion',
                              conocimientos_previos='conocimientos previos',
                              hard_soft='hard_soft', tutor=self.prof1,
                              cotutor=self.prof2)

        self.data_tfg_error = dict(titulo='titulo1',
                                   n_alumnos=2, descripcion='descripcion',
                                   conocimientos_previos='conocimientos previos',
                                   hard_soft='conocimientos previos', tutor=self.prof1,
                                   cotutor=self.prof2)

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
        data = {'file': ('ListaTFGs.xlsx', open(location, 'rb')), 'filas': 5, 'p_fila': 5,
                'cabeceras': json.dumps(dict(tipo='D', titulo='E',
                                  n_alumnos='F', descripcion='G',
                                  conocimientos_previos='H',
                                  hard_soft='I', tutor='B',
                                  cotutor='C'))}
        res = self.client.post('/upload_file_tfgs/', data, format='multipart')
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)
        self.assertEqual(resul['data'][1]['fila'], 8)
        self.assertEqual(resul['data'][1]['message'], 'El TFG no tiene titulo')
        self.assertEqual(resul['data'][0]['fila'], 6)
        self.assertEqual(resul['data'][0]['message'], 'El profesor no existe')
        res = self.client.login(username='jorgecasillas@ugr.es', password='75169052')
        self.assertEqual(res, True)
        res = self.client.get('/tfgs/', {'titulo': self.TFG1['titulo']})
        resul = json.loads(res.content)
        self.assertEqual(resul['status'], True)

