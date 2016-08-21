__author__ = 'tonima'
from tfgs.models import Tfg_Asig
from authentication.models import Departamento, Profesor
import itertools
from eventos.models import Tipo_Evento
from comisiones_evaluacion.models import Comision_Evaluacion, Tribunales
from comisiones_evaluacion.serializers import TribunalesSerializer, Comision_EvaluacionSerializer
import random
import math


DEPARTAMENTOS_PRINCIPALES = ['CCIA', 'LSI', 'ATC']
DEPARTAMENTOS_ASOCIADOS = {'ESTADISTICA': 'CCIA', 'ALGEBRA': 'CCIA', 'CN': 'LSI', 'TSTC': 'ATC'}
ORDEN_DEPARTAMENTOS = {0: 'LSI', 1: 'CCIA', 2: 'ATC'}


class Comision(object):

    def __init__(self, user, convocatoria, comisiones=None):
        self.tutores_principales = {'CCIA': [], 'LSI': [], 'ATC': []}
        self.tutores_libres = {'CCIA': [], 'LSI': [], 'ATC': []}
        self.exitos = []
        self.convocatoria = Tipo_Evento.objects.get(codigo=convocatoria)
        self.tfgs_asig = Tfg_Asig.objects.filter(convocatoria=self.convocatoria)
        self.comisiones = []
        self.num_tutores = 0
        self.num_tfg = self.tfgs_asig.count()
        self.num_comisiones = 0
        self.user = user
        self.reintentar = False
        if not comisiones:
            self.num_comisiones = 0
            for comision in Comision_Evaluacion.objects.all():
                serializer = Comision_EvaluacionSerializer(comision)
                serializer.delete(comision)
        else:
            comisiones = Comision_Evaluacion.objects.all()
            for key, comision in enumerate(comisiones):
                self.comisiones.append(comision.to_dict(user))
                self.comisiones[key]['tfgs'] = []
            self.num_comisiones = comisiones.count()

    def tutores_comisiones(self):
        try:
            self.departamentos = Departamento.objects.all()
            for tfg_asig in self.tfgs_asig:
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
            self.tutores_libres['CCIA'] = list(range(0, len(self.tutores_principales['CCIA'])))
            self.tutores_libres['LSI'] = list(range(0, len(self.tutores_principales['LSI'])))
            self.tutores_libres['ATC'] = list(range(0, len(self.tutores_principales['ATC'])))
            self.num_comisiones = int(math.ceil(self.num_tutores * 0.1))
            for i in range(self.num_comisiones):
                tribunal = {'tfgs': []}
                indice = random.randint(0, 2)
                departamento_1 = ORDEN_DEPARTAMENTOS[indice]
                departamento_2 = ORDEN_DEPARTAMENTOS[(indice + 1) % 3]
                departamento_3 = ORDEN_DEPARTAMENTOS[(indice + 2) % 3]
                presidente = random.choice(self.tutores_libres[departamento_1])
                self.tutores_libres[departamento_1].remove(presidente)
                vocal_1 = random.choice(self.tutores_libres[departamento_2])
                self.tutores_libres[departamento_2].remove(vocal_1)
                vocal_2 = random.choice(self.tutores_libres[departamento_3])
                self.tutores_libres[departamento_3].remove(vocal_2)
                tribunal['presidente'] = self.tutores_principales[departamento_1][presidente]
                tribunal['vocal_1'] = self.tutores_principales[departamento_2][vocal_1]
                tribunal['vocal_2'] = self.tutores_principales[departamento_3][vocal_2]
                self.comisiones.append(tribunal)
            self._seleccion_suplentes()
            self._guardar_comision()
            return dict(status=True, data=dict(num_comisiones=self.num_comisiones, num_tfg=self.num_tfg,
                                               num_tutores=self.num_tutores, tribunales=self.comisiones))
        except Exception as e:
                return dict(status=False, message=e)

    def _introducir_tutor(self, departamento, email):
        introducir = True
        for i in self.tutores_principales[departamento]:
            if i == email:
                introducir = False
                break
        if introducir:
            self.tutores_principales[departamento].append(email)
            self.num_tutores += 1

    def _check_tribunal(self, tribunal, tfg_asig, dict=False):
        if not dict:
            email = tfg_asig.tfg.tutor.email
        else:
            email = tfg_asig['tfg']['tutor']['email']
        if email in [tribunal.get('presidente'), tribunal.get('vocal_1'), tribunal.get('vocal_2'),
                     tribunal.get('suplente_1'), tribunal.get('suplente_2')] \
                or len(tribunal['tfgs']) >= (self.num_tfg / self.num_comisiones):
            return False
        else:
            return True

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
            suplente = ''
        return suplente

    def _seleccion_suplentes(self):
        for key, tribunal in enumerate(self.comisiones):
            indice = random.randint(0, 2)
            suplente_1 = self._seleccionar_suplente(indice)
            suplente_2 = self._seleccionar_suplente((indice + 1) % 3)
            self.comisiones[key]['suplente_1'] = suplente_1
            self.comisiones[key]['suplente_2'] = suplente_2

    def _guardar_comision(self):
        for i in self.comisiones:
            Comision_Evaluacion.objects.create(presidente=i['presidente'], vocal_1=i['vocal_1'], vocal_2=i['vocal_2'],
                                               suplente_1=i['suplente_1'], suplente_2=i['suplente_2'])

    def intercambiar(self, tfg):
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
            tribunal = Tribunales.objects.get(tfg=tfg_intercambiar['id'])
            serializer = TribunalesSerializer(tribunal)
            presidente = Profesor.objects.get(email=self.comisiones[tribunal_intercambiar]['presidente']['email'])
            serializer.update(tribunal, {'presidente': presidente})
            Tribunales.objects.create(tfg=tfg.tfg, comision=self.comisiones[tribunal_enc]['presidente']['email'])
        except:
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

    def asig_tfgs(self):
        try:
            for i in self.tfgs_asig:
                encontrado = False
                for key, tribunal in enumerate(self.comisiones):
                    if self._check_tribunal(tribunal, i):
                        self.comisiones[key]['tfgs'].append(i.to_dict(self.user))
                        Tribunales.objects.create(tfg=i.tfg, comision=self.comisiones[key].get('presidente').get('email'))
                        encontrado = True
                        break
                if not encontrado:
                    self.intercambiar(i)
            return dict(status=True, data=dict(tribunales=self.comisiones))
        except Exception as e:
                return dict(status=False, message=e)
