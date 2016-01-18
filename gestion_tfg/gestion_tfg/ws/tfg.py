__author__ = 'tonima'

from gestion_tfg.models import Tfg
from gestion_tfg.servicios import utils

def insert_tfg(request):
    """
    Insertar un tfg nuevo
    :param request:
    :return :
    """

    #TODO: Aqui va la comprobacion del perfil del usuario

    params = utils.get_param(request)

    return {'status': True, 'result': params}