from gestion_tfg.models import Tfg
from django.contrib.auth.models import User

def insert_tfg(tfg):

    # comprobando titulo vacio o Tfg con el mismo titulo
    if not tfg.titulo:
        return False
    else:
        res = Tfg.objects.filter(titulo=tfg.titulo)
        if res.count() != 0:
            return False

    # comprobando tipo no vacio
    if not tfg.tipo:
        return False

    # comprobando numero de alumnos
    if (tfg.n_alumnos is None) or (tfg.n_alumnos <= 0) or (tfg.n_alumnos > 3):
        return False

    #comprobando descripcion
    if not tfg.descripcion:
        return False

    #comprobando conocimientos previos
    if not tfg.conocimientos_previos:
        return False

    #comprobando requisitos HW SW
    if not tfg.hard_soft:
        return False

    #comprobando tutor
    if (not hasattr(tfg,'tutor')):
        return False

    #comprobando cotutor
    if (not hasattr(tfg,'cotutor')):
        return False

    tfg.save()
    return True

def update_tfg(tfg, campos):

    #comprobando titulo
    if 'titulo' in campos.keys():
        if campos['titulo'] == '' or not isinstance(campos['titulo'], str):
            return False
        else:
            tfg.titulo = campos['titulo']

    #comprobando tipo
    if 'tipo' in campos.keys():
        if campos['tipo'] == '' or not isinstance(campos['tipo'], str):
            return False
        else:
            tfg.tipo = campos['tipo']

    #comprobando n_alumnos
    if 'n_alumnos' in campos.keys():
        if (campos['n_alumnos'] <= 0) or (campos['n_alumnos'] > 3) or not(isinstance(campos['n_alumnos'], int)):
            return False
        else:
            tfg.n_alumnos = campos['n_alumnos']

    #comprobando descripcion
    if 'descripcion' in campos.keys():
        if campos['descripcion'] == '' or not isinstance(campos['descripcion'], str):
            return False
        else:
            tfg.descripcion = campos['descripcion']

    #comprobando conocimientos_previos
    if 'conocimientos_previos' in campos.keys():
        if campos['conocimientos_previos'] == '' or not isinstance(campos['conocimientos_previos'], str):
            return False
        else:
            tfg.conocimientos_previos = campos['conocimientos_previos']

    #comprobando hard_soft
    if 'hard_soft' in campos.keys():
        if campos['hard_soft'] == '' or not isinstance(campos['hard_soft'], str):
            return False
        else:
            tfg.hard_soft = campos['hard_soft']

    #comprobando tutor
    if 'tutor' in campos.keys():
        #NOTA: Cuando este el modelo de profesores, hay que ver que el tutor sea un profesor
        if not isinstance(campos['tutor'], User):
            return False
        else:
            tfg.tutor = campos['tutor']

    #comprobando cotutor
    if 'cotutor' in campos.keys():
        #NOTA: Cuando este el modelo de profesores, hay que ver que el tutor sea un profesor
        if not isinstance(campos['cotutor'], User):
            return False
        else:
            tfg.tutor = campos['cotutor']

    tfg.save()

    return True

def delete_tfg(tfg):

    tfg.delete()

    try:
        Tfg.objects.get(titulo=tfg)
        return True
    except Tfg.DoesNotExist:
        return False
