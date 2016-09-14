from __future__ import division
from tfgs.models import Tfg_Asig
from authentication.models import Departamento, Profesor, Titulacion
import itertools
from eventos.models import Tipo_Evento, Convocatoria, SubTipo_Evento
from comisiones_evaluacion.models import Comision_Evaluacion, Tribunales
from comisiones_evaluacion.serializers import TribunalesSerializer, Comision_EvaluacionSerializer
from gestfg.settings import DOC_PATH
import random
import math
import hashlib as hl
import random
import zipfile
import os
import sys

DEPARTAMENTOS_PRINCIPALES = ['DECSAI', 'LSI', 'ATC']
DEPARTAMENTOS_ASOCIADOS = {'ESTADISTICA': 'DECSAI', 'AL': 'DECSAI', 'AM': 'DECSAI', 'TSTC': 'ATC', 'ELECTRONICA': 'ATC', 'MATEAPLI': 'LSI', 'EMPRESAS': 'LSI'}
ORDEN_DEPARTAMENTOS = {0: 'LSI', 1: 'DECSAI', 2: 'ATC'}

TESTING = sys.argv[1:2] == ['test']


class Comision(object):

    def __init__(self, user, convocatoria, anio, titulacion, comisiones=None):
        self.tutores_principales = {'DECSAI': [], 'LSI': [], 'ATC': []}
        self.tutores_secundarios = {'DECSAI': [], 'LSI': [], 'ATC': []}
        self.tutores_libres = {'DECSAI': [], 'LSI': [], 'ATC': []}
        self.tutores_libres_secundarios = {'DECSAI': [], 'LSI': [], 'ATC': []}
        self.exitos = []
        self.anio = int(anio)
        self.titulacion = Titulacion.objects.get(codigo=titulacion)
        self.convocatoria = Convocatoria.objects.get(titulacion=self.titulacion,
                                                     subtipo=SubTipo_Evento.objects.get(codigo='COM_EVAL'),
                                                     tipo=Tipo_Evento.objects.get(codigo=convocatoria),
                                                     anio=anio)
        self.convocatoria_tfgs = Convocatoria.objects.get(titulacion=self.titulacion,
                                                          subtipo=SubTipo_Evento.objects.get(codigo='SOL_EVAL'),
                                                          tipo=Tipo_Evento.objects.get(codigo=convocatoria),
                                                          anio=anio)
        self.tfgs_asig_conv = Tfg_Asig.objects.filter(convocatoria=self.convocatoria_tfgs)
        self.tfgs_asig = Tfg_Asig.objects.all()
        self.comisiones = []
        self.num_tutores = 0
        self.num_tfg = self.tfgs_asig_conv.count()
        self.num_comisiones = 0
        self.user = user
        self.reintentar = False
        if TESTING:
            self.num_tfg_comision = 6.0
        else:
            self.num_tfg_comision = 5.0
        if not comisiones:
            self.num_comisiones = 0
            for comision in Comision_Evaluacion.objects.all():
                serializer = Comision_EvaluacionSerializer(comision)
                serializer.delete(comision)
        else:
            comisiones = Comision_Evaluacion.objects.filter(convocatoria=self.convocatoria)
            for key, comision in enumerate(comisiones):
                self.comisiones.append(comision.to_dict(user))
                self.comisiones[key]['tfgs'] = []
            self.num_comisiones = comisiones.count()

            for tribunal in Tribunales.objects.all():
                if tribunal.comision in comisiones:
                    serializer = TribunalesSerializer(tribunal)
                    serializer.delete(tribunal)

    def tutores_comisiones(self):
        try:
            self.departamentos = Departamento.objects.all()
            for tfg_asig in self.tfgs_asig_conv:
                try:
                    if tfg_asig.tfg.tutor.departamento.codigo in DEPARTAMENTOS_PRINCIPALES:
                        self._introducir_tutor(tfg_asig.tfg.tutor.departamento.codigo, tfg_asig.tfg.tutor.email)
                    else:
                        dep_asociado = DEPARTAMENTOS_ASOCIADOS[tfg_asig.tfg.tutor.departamento.codigo]
                        self._introducir_tutor(dep_asociado, tfg_asig.tfg.tutor.email)
                    if tfg_asig.tfg.cotutor:
                        if tfg_asig.tfg.cotutor.departamento.codigo in DEPARTAMENTOS_PRINCIPALES:
                            self._introducir_tutor(tfg_asig.tfg.cotutor.departamento.codigo, tfg_asig.tfg.cotutor.email)
                        else:
                            dep_asociado = DEPARTAMENTOS_ASOCIADOS[tfg_asig.tfg.cotutor.departamento.codigo]
                            self._introducir_tutor(dep_asociado, tfg_asig.tfg.cotutor.email)
                except KeyError as e:
                    pass
            for tfg_asig in self.tfgs_asig:
                try:
                    if tfg_asig.tfg.tutor.departamento.codigo in DEPARTAMENTOS_PRINCIPALES:
                        self._introducir_tutor_secundario(tfg_asig.tfg.tutor.departamento.codigo, tfg_asig.tfg.tutor.email)
                    else:
                        dep_asociado = DEPARTAMENTOS_ASOCIADOS[tfg_asig.tfg.tutor.departamento.codigo]
                        self._introducir_tutor_secundario(dep_asociado, tfg_asig.tfg.tutor.email)
                    if tfg_asig.tfg.cotutor:
                        if tfg_asig.tfg.cotutor.departamento.codigo in DEPARTAMENTOS_PRINCIPALES:
                            self._introducir_tutor_secundario(tfg_asig.tfg.cotutor.departamento.codigo, tfg_asig.tfg.cotutor.email)
                        else:
                            dep_asociado = DEPARTAMENTOS_ASOCIADOS[tfg_asig.tfg.cotutor.departamento.codigo]
                            self._introducir_tutor_secundario(dep_asociado, tfg_asig.tfg.cotutor.email)
                except KeyError as e:
                    pass
            self.tutores_libres['DECSAI'] = list(range(0, len(self.tutores_principales['DECSAI'])))
            self.tutores_libres['LSI'] = list(range(0, len(self.tutores_principales['LSI'])))
            self.tutores_libres['ATC'] = list(range(0, len(self.tutores_principales['ATC'])))
            self.tutores_libres_secundarios['DECSAI'] = list(range(0, len(self.tutores_secundarios['DECSAI'])))
            self.tutores_libres_secundarios['LSI'] = list(range(0, len(self.tutores_secundarios['LSI'])))
            self.tutores_libres_secundarios['ATC'] = list(range(0, len(self.tutores_secundarios['ATC'])))
            self.num_comisiones = int(math.ceil(float(self.num_tfg) / self.num_tfg_comision) if self.num_tfg >= 12 else 2)
            for i in range(self.num_comisiones):
                tribunal = {'tfgs': []}
                indice = random.randint(0, 2)
                departamento_1 = ORDEN_DEPARTAMENTOS[indice]
                departamento_2 = ORDEN_DEPARTAMENTOS[(indice + 1) % 3]
                departamento_3 = ORDEN_DEPARTAMENTOS[(indice + 2) % 3]
                tribunal['presidente'] = self._elegir_miembro(departamento_1)
                tribunal['vocal_1'] = self._elegir_miembro(departamento_2)
                tribunal['vocal_2'] = self._elegir_miembro(departamento_3)
                self.comisiones.append(tribunal)
            self._seleccion_suplentes()
            self._guardar_comision()
            return dict(status=True, data=dict(num_comisiones=self.num_comisiones, num_tfg=self.num_tfg,
                                               num_tutores=self.num_tutores, tribunales=self.comisiones,
                                               titulacion=self.titulacion.to_dict()))


        except Exception as e:
                return dict(status=False, message=e)

    def _elegir_miembro(self, departamento):
        if len(self.tutores_libres[departamento]) > 0:
            vocal_2 = random.choice(self.tutores_libres[departamento])
            self.tutores_libres[departamento].remove(vocal_2)
            return self.tutores_principales[departamento][vocal_2]
        else:
            vocal_2 = random.choice(self.tutores_libres_secundarios[departamento])
            self.tutores_libres_secundarios[departamento].remove(vocal_2)
            return self.tutores_secundarios[departamento][vocal_2]

    def _check_tutores_principales(self, email):
        return any(email in e for e in [self.tutores_principales['LSI'], self.tutores_principales['ATC'],
                                        self.tutores_principales['DECSAI']])

    def _introducir_tutor(self, departamento, email):
        introducir = True
        for i in self.tutores_principales[departamento]:
            if i == email:
                introducir = False
                break
        if introducir:
            self.tutores_principales[departamento].append(email)
            self.num_tutores += 1

    def _introducir_tutor_secundario(self, departamento, email):
        introducir = True
        if not self._check_tutores_principales(email):
            for i in self.tutores_secundarios[departamento]:
                if i == email:
                    introducir = False
                    break
            if introducir:
                self.tutores_secundarios[departamento].append(email)
                self.num_tutores += 1

    def _check_tribunal(self, tribunal, tfg_asig, dict=False):
        if not dict:
            email = tfg_asig.tfg.tutor.email
        else:
            email = tfg_asig['tfg']['tutor']['email']
        if email in [tribunal.get('presidente').get('email'), tribunal.get('vocal_1').get('email'), tribunal.get('vocal_2').get('email'),
                     tribunal.get('suplente_1').get('email'), tribunal.get('suplente_2').get('email')] \
                or len(tribunal['tfgs']) >= (self.num_tfg / self.num_comisiones):
            return False
        else:
            return True

    # para seleccionar un suplente primero miro en los tutores principales y si no en los secundarios
    def _seleccionar_suplente(self, indice):
        if len(self.tutores_libres[ORDEN_DEPARTAMENTOS[indice]]) > 0:
            departamento = ORDEN_DEPARTAMENTOS[indice]
            ind_suplente_1 = self.tutores_libres[departamento][0]
            suplente = self.tutores_principales[ORDEN_DEPARTAMENTOS[indice]][ind_suplente_1]
            self.tutores_libres[ORDEN_DEPARTAMENTOS[indice]].pop(0)
        elif len(self.tutores_libres[ORDEN_DEPARTAMENTOS[(indice + 1) % 3]]) > 0:
            departamento = ORDEN_DEPARTAMENTOS[(indice + 1) % 3]
            ind_suplente_1 = self.tutores_libres[departamento][0]
            suplente = self.tutores_principales[departamento][ind_suplente_1]
            self.tutores_libres[ORDEN_DEPARTAMENTOS[(indice + 1) % 3]].pop(0)
        elif len(self.tutores_libres[ORDEN_DEPARTAMENTOS[(indice + 2) % 3]]) > 0:
            departamento = ORDEN_DEPARTAMENTOS[(indice + 2) % 3]
            ind_suplente_1 = self.tutores_libres[departamento][0]
            suplente = self.tutores_principales[departamento][ind_suplente_1]
            self.tutores_libres[ORDEN_DEPARTAMENTOS[(indice + 2) % 3]].pop(0)
        else:
            if len(self.tutores_libres_secundarios[ORDEN_DEPARTAMENTOS[indice]]) > 0:
                departamento = ORDEN_DEPARTAMENTOS[indice]
                ind_suplente_1 = self.tutores_libres_secundarios[departamento][0]
                suplente = self.tutores_secundarios[ORDEN_DEPARTAMENTOS[indice]][ind_suplente_1]
                self.tutores_libres_secundarios[ORDEN_DEPARTAMENTOS[indice]].pop(0)
            elif len(self.tutores_libres_secundarios[ORDEN_DEPARTAMENTOS[(indice + 1) % 3]]) > 0:
                departamento = ORDEN_DEPARTAMENTOS[(indice + 1) % 3]
                ind_suplente_1 = self.tutores_libres_secundarios[departamento][0]
                suplente = self.tutores_secundarios[departamento][ind_suplente_1]
                self.tutores_libres_secundarios[ORDEN_DEPARTAMENTOS[(indice + 1) % 3]].pop(0)
            elif len(self.tutores_libres_secundarios[ORDEN_DEPARTAMENTOS[(indice + 2) % 3]]) > 0:
                departamento = ORDEN_DEPARTAMENTOS[(indice + 2) % 3]
                ind_suplente_1 = self.tutores_libres_secundarios[departamento][0]
                suplente = self.tutores_secundarios[departamento][ind_suplente_1]
                self.tutores_libres_secundarios[ORDEN_DEPARTAMENTOS[(indice + 2) % 3]].pop(0)
        return suplente

    def _seleccion_suplentes(self):
        for key, tribunal in enumerate(self.comisiones):
            indice = random.randint(0, 2)
            suplente_1 = self._seleccionar_suplente(indice)
            suplente_2 = self._seleccionar_suplente((indice + 1) % 3)
            self.comisiones[key]['suplente_1'] = suplente_1
            self.comisiones[key]['suplente_2'] = suplente_2

    def _guardar_comision(self):
        for key, i in enumerate(self.comisiones):
            comision = Comision_Evaluacion.objects.create(presidente=i['presidente'], vocal_1=i['vocal_1'],
                                                          vocal_2=i['vocal_2'], suplente_1=i['suplente_1'],
                                                          suplente_2=i['suplente_2'], convocatoria=self.convocatoria)
            self.comisiones[key] = comision['data'].to_dict(self.user)

    def intercambiar(self, tfg, alumno):
        try:
            tribunal_enc = None
            for key, tribunal in enumerate(self.comisiones):
                if tfg.tfg.tutor.email not in [tribunal.get('presidente').get('email'),
                                               tribunal.get('vocal_1').get('email'),
                                               tribunal.get('vocal_2').get('email'),
                                               tribunal.get('suplente_1').get('email'),
                                               tribunal.get('suplente_2').get('email')]:
                    tribunal_enc = key
                    break
            tribunal_intercambiar, tfg_intercambiar = self.bucar_tfg_intercambiar(tribunal_enc)
            self.comisiones[tribunal_intercambiar]['tfgs'].append(tfg_intercambiar)
            self.comisiones[tribunal_enc]['tfgs'].remove(tfg_intercambiar)
            self.comisiones[tribunal_enc]['tfgs'].append(tfg.to_dict(self.user))
            tribunal = Tribunales.objects.filter(tfg=tfg_intercambiar['id']) # TODO comprobar esto
            serializer = TribunalesSerializer(tribunal[0])
            presidente = Profesor.objects.get(email=self.comisiones[tribunal_intercambiar]['presidente']['email'])
            serializer.update(self.user, tribunal[0], {'presidente': presidente})
            Tribunales.objects.create(tfg=tfg.tfg, comision=self.comisiones[tribunal_enc]['presidente']['email'], alumno=alumno)
        except Exception as e:
            self.reintentar = True

    def bucar_tfg_intercambiar(self, tribunal_key):
        for tfg in self.comisiones[tribunal_key]['tfgs']:
            for key, tribunal in enumerate(self.comisiones):
                if key is not tribunal_key and tfg['tfg']['tutor']['email'] not in [tribunal.get('presidente').get('email'),
                                                                                    tribunal.get('vocal_1').get('email'),
                                                                                    tribunal.get('vocal_2').get('email'),
                                                                                    tribunal.get('suplente_1').get('email'),
                                                                                    tribunal.get('suplente_2').get('email')]:
                    return key, tfg

    def _create_tribunal(self, tfg_asig, alumno):
        encontrado = False
        for key, tribunal in enumerate(self.comisiones):
            if self._check_tribunal(tribunal, tfg_asig):
                self.comisiones[key]['tfgs'].append(tfg_asig.to_dict(self.user))
                Tribunales.objects.create(tfg=tfg_asig.tfg, comision=self.comisiones[key].get('presidente').get('email'),
                                          alumno=alumno)
                encontrado = True
                break
        if not encontrado:
            self.intercambiar(tfg_asig, alumno)

    def asig_tfgs(self):
        try:
            for i in self.tfgs_asig_conv:
                self._create_tribunal(i, i.alumno_1)
                if i.alumno_2:
                    self._create_tribunal(i, i.alumno_2)
                if i.alumno_3:
                    self._create_tribunal(i, i.alumno_3)
            return dict(status=True, data=dict(tribunales=self.comisiones))
        except Exception as e:
                return dict(status=False, message=e)


class Tribunal(object):

    def __init__(self, user, tribunal):
        self.user = user
        self.tribunal = tribunal

    def upload_doc(self, fichero):
        if not zipfile.is_zipfile(fichero):
            raise NameError('El fichero no tiene el formato correcto')

        # calcular nombre del fichero
        hash_fichero = hl.sha256()
        hash_fichero.update(fichero.name)
        hash_fichero.update('%6.6f' % random.randint(0, 999999))

        nombre_fichero = hash_fichero.hexdigest()

        fichero.file.seek(0)
        with file(os.path.join(DOC_PATH, nombre_fichero), 'wb') as f:
            f.write(fichero.file.read())

        self.tribunal.documentacion = nombre_fichero
        self.tribunal.save()

        return dict(status=True, data=self.tribunal.to_dict(self.user))
