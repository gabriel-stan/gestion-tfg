__author__ = 'tonima'
from openpyxl import load_workbook
from authentication.models import Profesor, Alumno
from tfgs.models import Titulacion, Tfg_Asig, Tfg


def upload_file_tfg(fichero, u_fila, p_fila, cabeceras):
    wb = load_workbook(fichero)
    ws = wb.active
    errores = []
    exitos = []
    for i in range(p_fila, u_fila+1):
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


def upload_file_tfg_preasig(fichero, u_fila, p_fila, cabeceras):
    wb = load_workbook(fichero)
    ws = wb.active
    errores = []
    exitos = []
    for i in range(p_fila, u_fila+1):
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
            if Tfg.objects.simular_create_tfg(**tfg):
                datos['alumno_1'] = Alumno.objects.get(email=str(ws[cabeceras['alumno_1'] + str(i)].value))
                datos['alumno_2'] = Alumno.objects.get(email=str(ws[cabeceras['alumno_2'] + str(i)].value)) if (cabeceras.get('alumno_2') != None and ws[cabeceras['alumno_2'] + str(i)].value != None) else None
                datos['alumno_3'] = Alumno.objects.get(email=str(ws[cabeceras['alumno_3'] + str(i)].value)) if (cabeceras.get('alumno_3') != None and ws[cabeceras['alumno_3'] + str(i)].value != None) else None
                tfg = Tfg(tipo=datos['tipo'], titulo=datos['titulo'], n_alumnos=datos['n_alumnos'],
                           descripcion=datos['descripcion'], conocimientos_previos=datos['conocimientos_previos'],
                           hard_soft=datos['hard_soft'], tutor=datos['tutor'], titulacion=datos['titulacion'])
                tfg_asig = dict(tfg=tfg, alumno_1=datos['alumno_1'], alumno_2=datos['alumno_2'],
                                alumno_3=datos['alumno_3'])
                if Tfg_Asig.objects.simular_create_tfg_asig(**tfg_asig):
                    exitos.append(dict(fila=i, tfg=tfg_asig))
        except Profesor.DoesNotExist:
            errores.append(dict(fila=i, message='El profesor no existe'))
            continue
        except Alumno.DoesNotExist:
            errores.append(dict(fila=i, message='El alumno no existe'))
            continue
        except Titulacion.DoesNotExist:
            errores.append(dict(fila=i, message='La titulacion no existe'))
            continue
        except Exception as e:
            errores.append(dict(fila=i, message=e.message))
            continue
    return dict(status=True, data=errores)
