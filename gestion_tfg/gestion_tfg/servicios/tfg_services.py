from gestion_tfg.models import Tfg


def insert_tfg(tfg):

    save = True


    if (tfg.n_alumnos is None) or (not hasattr(tfg,'tutor')) or (not hasattr(tfg,'cotutor')):
        save = False

    if save:
        print("ha pasado")
        tfg.save()
        return True
    else:
        return False