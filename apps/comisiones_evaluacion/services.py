__author__ = 'tonima'
from tfgs.models import Tfg_Asig
from authentication.models import Departamento, Profesor
import itertools

DEPARTAMENTOS_PRINCIPALES = ['CCIA', 'LSI', 'ATC']
DEPARTAMENTOS_ASOCIADOS = {'CCIA': [], 'LSI': [], 'ATC':[]}


class Comision(object):

    def __init__(self):
        self.tutores_principales = {'CCIA': [], 'LSI': [], 'ATC':[]}
        self.exitos = []

    def tutores_comisiones(self, convocatoria):
        try:
            self.departamentos = Departamento.objects.all()
            for tfg_asig in Tfg_Asig.objects.filter(convocatoria=convocatoria):
                if tfg_asig.tfg.tutor.departamento.codigo in DEPARTAMENTOS_PRINCIPALES:
                    self.tutores_principales[tfg_asig.tfg.tutor.departamento.codigo].append(tfg_asig.tfg.tutor.email)

        except Exception as e:
                return dict(status=False, message=e)
