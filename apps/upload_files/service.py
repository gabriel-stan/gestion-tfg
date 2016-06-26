__author__ = 'tonima'
from openpyxl import load_workbook
from authentication.models import Profesor
from tfgs.models import Titulacion
from tfgs.models import Tfg


def upload_file_tfg(fichero, filas, p_fila, cabeceras):
    wb = load_workbook(fichero)
    ws = wb.active
    errores = []
    exitos = []
    for i in range(p_fila, 5+filas):
        try:
            datos = dict(tipo=ws[cabeceras['tipo'] + str(i)].value,
                         titulo=ws[cabeceras['titulo'] + str(i)].value,
                         n_alumnos=ws[cabeceras['n_alumnos'] + str(i)].value,
                         descripcion=ws[cabeceras['descripcion'] + str(i)].value,
                         conocimientos_previos=ws[cabeceras['conocimientos_previos'] + str(i)].value,
                         hard_soft=ws[cabeceras['hard_soft'] + str(i)].value,
                         titulacion=ws[cabeceras['titulacion'] + str(i)].value)
            if not datos['titulo']:
                errores.append(dict(fila=i, message='El TFG no tiene titulo'))
                continue
            datos['tutor'] = Profesor.objects.get(email=str(ws[cabeceras['tutor'] + str(i)].value))
            if ws[cabeceras['cotutor'] + str(i)].value:
                datos['cotutor'] = Profesor.objects.get(emailyes=str(ws[cabeceras['cotutor'] + str(i)].value))
                tfg = dict(tipo=datos['tipo'], titulo=datos['titulo'], n_alumnos=datos['n_alumnos'],
                           descripcion=datos['descripcion'], conocimientos_previos=datos['conocimientos_previos'],
                           hard_soft=datos['hard_soft'],
                           tutor=datos['tutor'].email, cotutor=datos['cotutor'].email, titulacion=datos['titulacion'])
            else:
                tfg = dict(tipo=datos['tipo'], titulo=datos['titulo'], n_alumnos=datos['n_alumnos'],
                           descripcion=datos['descripcion'], conocimientos_previos=datos['conocimientos_previos'],
                           hard_soft=datos['hard_soft'],
                           tutor=datos['tutor'].email, titulacion=datos['titulacion'])
            if Tfg.objects.simular_create_tfg(**tfg):
                exitos.append(dict(fila=i, tfg=tfg))
        except Profesor.DoesNotExist:
            errores.append(dict(fila=i, message='El profesor no existe'))
            continue
        except Titulacion.DoesNotExist:
            errores.append(dict(fila=i, message='La titulacion no existe'))
            continue
        except Exception as e:
            errores.append(dict(fila=i, message=e.message))
            continue
    return dict(status=True, exitos=exitos, errores=errores)


def upload_file_confirm(tfgs, model):
    errores = []
    for index, data_tfg in enumerate(tfgs):
        try:
            tfg = data_tfg.get('tfg')
            res = model.objects.create(**tfg)
            if not res.get('status'):
                errores.append(dict(fila=index, tfg=tfg))
        except Exception as e:
            errores.append(dict(fila=index, message=e.message))
            continue
    return dict(status=True, errores=errores)


def upload_file_tfg_preasig(fichero, filas, p_fila, cabeceras):
    wb = load_workbook(fichero)
    ws = wb.active
    errores = []
    for i in range(p_fila, 5+filas):
        try:
            datos = dict(tipo=ws[cabeceras['tipo'] + str(i)].value,
                         titulo=ws[cabeceras['titulo'] + str(i)].value,
                         n_alumnos=ws[cabeceras['n_alumnos'] + str(i)].value,
                         descripcion=ws[cabeceras['descripcion'] + str(i)].value,
                         conocimientos_previos=ws[cabeceras['conocimientos_previos'] + str(i)].value,
                         hard_soft=ws[cabeceras['hard_soft'] + str(i)].value,
                         titulacion=ws[cabeceras['titulacion'] + str(i)].value)
            if not datos['titulo']:
                errores.append(dict(fila=i, message='El TFG no tiene titulo'))
                continue
            datos['tutor'] = Profesor.objects.get(email=str(ws[cabeceras['tutor'] + str(i)].value))
            if ws[cabeceras['cotutor'] + str(i)].value:
                datos['cotutor'] = Profesor.objects.get(emailyes=str(ws[cabeceras['cotutor'] + str(i)].value))
                tfg = dict(tipo=datos['tipo'], titulo=datos['titulo'], n_alumnos=datos['n_alumnos'],
                           descripcion=datos['descripcion'], conocimientos_previos=datos['conocimientos_previos'],
                           hard_soft=datos['hard_soft'], tutor=datos['tutor'], cotutor=datos['cotutor'],
                           titulacion=datos['titulacion'])
            else:
                tfg = dict(tipo=datos['tipo'], titulo=datos['titulo'], n_alumnos=datos['n_alumnos'],
                           descripcion=datos['descripcion'], conocimientos_previos=datos['conocimientos_previos'],
                           hard_soft=datos['hard_soft'], tutor=datos['tutor'], titulacion=datos['titulacion'])
            Tfg.objects.create_tfg(**tfg)
        except Profesor.DoesNotExist:
            errores.append(dict(fila=i, message='El profesor no existe'))
            continue
        except Titulacion.DoesNotExist:
            errores.append(dict(fila=i, message='La titulacion no existe'))
            continue
        except Exception as e:
            errores.append(dict(fila=i, message=e.message))
            continue
    return dict(status=True, data=errores)
