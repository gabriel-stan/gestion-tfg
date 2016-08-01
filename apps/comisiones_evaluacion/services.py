__author__ = 'tonima'
from tfgs.models import Tfg_Asig
from authentication.models import Departamento, Profesor
import itertools
from eventos.models import Tipo_Evento
import random
import math


DEPARTAMENTOS_PRINCIPALES = ['CCIA', 'LSI', 'ATC']
DEPARTAMENTOS_ASOCIADOS = {'ESTADISTICA': 'CCIA', 'ALGEBRA': 'CCIA', 'CN': 'LSI', 'TSTC': 'ATC'}
ORDEN_DEPARTAMENTOS = {0: 'LSI', 1: 'CCIA', 2: 'ATC'}


class Comision(object):

    def __init__(self):
        self.tutores_principales = {'CCIA': [], 'LSI': [], 'ATC': []}
        self.tutores_libres = {'CCIA': [], 'LSI': [], 'ATC': []}
        self.exitos = []
        self.tribunales = []
        self.num_tutores = 0
        self.num_tfg = 0
        self.num_tribunales = 0

    def tutores_comisiones(self, convocatoria):
        try:
            self.departamentos = Departamento.objects.all()
            convocatoria = Tipo_Evento.objects.get(codigo=convocatoria)
            self.tfgs_asig = Tfg_Asig.objects.filter(convocatoria=convocatoria)
            for tfg_asig in self.tfgs_asig:
                if tfg_asig.tfg.tutor.departamento.codigo in DEPARTAMENTOS_PRINCIPALES:
                    self.tutores_principales[tfg_asig.tfg.tutor.departamento.codigo].append(tfg_asig.tfg.tutor.email)
                else:
                    dep_asociado = DEPARTAMENTOS_ASOCIADOS[tfg_asig.tfg.tutor.departamento.codigo]
                    self.tutores_principales[dep_asociado].append(tfg_asig.tfg.tutor.email)
                self.num_tutores += 1
            self.tutores_libres['CCIA'] = list(range(0, len(self.tutores_principales['CCIA'])))
            self.tutores_libres['LSI'] = list(range(0, len(self.tutores_principales['LSI'])))
            self.tutores_libres['ATC'] = list(range(0, len(self.tutores_principales['ATC'])))
            self.num_tfg = self.tfgs_asig.count()
            self.num_tribunales = int(math.ceil(self.num_tutores * 0.1)) + 1
            return {'status', True}
        except Exception as e:
                return dict(status=False, message=e)

    def check_tribunal(self, tribunal, tfg_asig):
        if tfg_asig.tfg.tutor.email in [tribunal.get('presidente'), tribunal.get('vocal_1'), tribunal.get('vocal_2')]:
            return False
        else:
            return True

    def asig_tfgs(self):
        try:
            for i in range(self.num_tribunales):
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
                self.tribunales.append(tribunal)
                for i in self.tfgs_asig:
                    for key, tribunal in enumerate(self.tribunales):
                        if self.check_tribunal(tribunal, i):
                            self.tribunales[key]['tfgs'].append(i)
                            break
        except Exception as e:
                return dict(status=False, message=e)
