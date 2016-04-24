__author__ = 'tonima'
from rest_framework.decorators import api_view
from rest_framework.response import Response
import simplejson as json

from controller.servicios import tfg_services
from model.models import Tfg


@api_view(['POST'])
def upload_file(request):
    """
    Carga masiva de TFGs mediante un fichero en .xlsx
    :param request: tfg <str>, campos <dict>
    :return :
    """

    # TODO: Aqui va la comprobacion del perfil del usuario que quiere actualizar
    try:
        if request.method == 'POST':
            file = request.FILES['file']
            filas = int(request.POST['filas'])
            p_fila = int(request.POST['p_fila'])
            cabeceras = json.loads(request.POST['cabeceras'])
            resul = tfg_services.subida_masiva(file, filas, p_fila, cabeceras)
            return Response(resul)

    except Tfg.DoesNotExist:
        return Response(dict(status=False, message="El tfg indicado no existe"))
    except Exception:
        return Response(dict(status=False, message="Error en la llamada"))
