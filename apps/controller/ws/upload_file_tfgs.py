__author__ = 'tonima'
from rest_framework.decorators import api_view
from rest_framework.response import Response
from controller.servicios import tfg_services, utils
from model.models import Tfg


@api_view(['POST'])
def upload_file(request):
    """
    Carga masiva de TFGs mediante un fichero en .ods
    :param request: tfg <str>, campos <dict>
    :return :
    """

    # TODO: Aqui va la comprobacion del perfil del usuario que quiere actualizar
    try:
        if request.method == 'POST':
            file = request.FILES['file']
            filas = int(request.POST['filas'])
            resul = tfg_services.subida_masiva(file,filas)
            return Response(resul)

    except Tfg.DoesNotExist:
        return Response(dict(status=False, message="El tfg indicado no existe"))
    except Exception:
        return Response(dict(status=False, message="Error en la llamada"))
