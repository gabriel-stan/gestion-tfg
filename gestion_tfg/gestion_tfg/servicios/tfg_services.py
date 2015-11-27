from gestion_tfg.models import Tfg


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
