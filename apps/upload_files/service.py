__author__ = 'tonima'
from openpyxl import load_workbook
from authentication.models import Profesor, Alumno
from tfgs.models import Titulacion, Tfg_Asig, Tfg


class Tfgs_masivos(object):

    def __init__(self, fichero):
        self.wb = load_workbook(fichero)
        self.ws = self.wb.active
        self.errores = []
        self.exitos = []

    def upload_file_tfg(self, u_fila, p_fila, cabeceras):
        for i in range(p_fila, u_fila+1):
            try:
                data_tfg = self.read_data(cabeceras, i)
                tfg = self.check_tfg(data_tfg, i)
                if tfg != False and Tfg.objects.simular_create_tfg(**tfg):
                    self.exitos.append(dict(fila=i, tfg=tfg))
            except Profesor.DoesNotExist:
                self.errores.append(dict(fila=i, message='El profesor no existe'))
                continue
            except Titulacion.DoesNotExist:
                self.errores.append(dict(fila=i, message='La titulacion no existe'))
                continue
            except Exception as e:
                self.errores.append(dict(fila=i, message=e.message))
                continue
        return dict(status=True, exitos=self.exitos, errores=self.errores)

    def read_data(self, cabeceras, i):
        resul = dict(tipo=self.ws[cabeceras['tipo'] + str(i)].value,
                     titulo=self.ws[cabeceras['titulo'] + str(i)].value,
                     n_alumnos=self.ws[cabeceras['n_alumnos'] + str(i)].value,
                     descripcion=self.ws[cabeceras['descripcion'] + str(i)].value,
                     conocimientos_previos=
                     self.ws[cabeceras['conocimientos_previos'] + str(i)].value,
                     hard_soft=self.ws[cabeceras['hard_soft'] + str(i)].value,
                     titulacion=self.ws[cabeceras['titulacion'] + str(i)].value,
                     tutor=self.ws[cabeceras['tutor'] + str(i)].value,
                     cotutor=self.ws[cabeceras['cotutor'] + str(i)].value)

        return resul

    def check_tfg(self, tfg, i):
        if not tfg.get('titulo'):
            self.errores.append(dict(fila=i, message='El TFG no tiene titulo'))
            return False
        tfg['tutor'] = Profesor.objects.get(email=tfg.get('tutor'))
        tfg['titulacion'] = Titulacion.objects.get(codigo=tfg.get('titulacion'))
        if tfg.get('cotutor'):
            tfg['cotutor'] = Profesor.objects.get(email=str(tfg.get('cotutor')))
            tfg = dict(tipo=tfg['tipo'], titulo=tfg['titulo'], n_alumnos=tfg['n_alumnos'],
                       descripcion=tfg['descripcion'], conocimientos_previos=tfg['conocimientos_previos'],
                       hard_soft=tfg['hard_soft'],
                       tutor=tfg['tutor'].email, cotutor=tfg['cotutor'].email, titulacion=tfg['titulacion'].codigo)
        else:
            tfg = dict(tipo=tfg['tipo'], titulo=tfg['titulo'], n_alumnos=tfg['n_alumnos'],
                       descripcion=tfg['descripcion'], conocimientos_previos=tfg['conocimientos_previos'],
                       hard_soft=tfg['hard_soft'],
                       tutor=tfg['tutor'].email, titulacion=tfg['titulacion'].codigo)
            return tfg


class Tfgs_asig_masivos(Tfgs_masivos):

    def __init__(self, fichero):
        super(Tfgs_asig_masivos, self).__init__(fichero)

    def upload_file_tfg(self, u_fila, p_fila, cabeceras):
        for i in range(p_fila, u_fila+1):
            try:
                data_tfg = self.read_data(cabeceras, i)
                self.tfg = self.check_tfg(data_tfg, i)
                if self.tfg != False and Tfg.objects.simular_create_tfg(**self.tfg):
                    model_tfg = Tfg(**data_tfg)
                    self.check_tfg_asig(data_tfg, cabeceras, i)
                    tfg_asig = dict(tfg=model_tfg, alumno_1=data_tfg['alumno_1'], alumno_2=data_tfg['alumno_2'],
                                    alumno_3=data_tfg['alumno_3'])
                    if Tfg_Asig.objects.simular_create_tfg_asig(**tfg_asig):
                        self.exitos.append(dict(fila=i, tfg=self.tfg))
            except Profesor.DoesNotExist:
                self.errores.append(dict(fila=i, message='El profesor no existe'))
                continue
            except Alumno.DoesNotExist:
                self.errores.append(dict(fila=i, message='El alumno no existe'))
                continue
            except Titulacion.DoesNotExist:
                self.errores.append(dict(fila=i, message='La titulacion no existe'))
                continue
            except Exception as e:
                self.errores.append(dict(fila=i, message=e.message))
                continue
        return dict(status=True, exitos=self.exitos, errores=self.errores)

    def check_tfg_asig(self, data_tfg, cabeceras, i):
        data_tfg['alumno_1'] = Alumno.objects.get(email=unicode(self.ws[cabeceras['alumno_1'] + str(i)].value if cabeceras.get('alumno_1') else None))
        self.tfg['alumno_1'] = data_tfg.get('alumno_1').email if data_tfg.get('alumno_1') else None

        data_tfg['alumno_2'] = Alumno.objects.get(email=unicode(self.ws[cabeceras['alumno_2'] + str(i)].value)) if (
            cabeceras.get('alumno_2') and self.ws[cabeceras['alumno_2'] + str(i)].value) else None
        self.tfg['alumno_2'] = data_tfg.get('alumno_2').email if data_tfg.get('alumno_2') else None

        data_tfg['alumno_3'] = Alumno.objects.get(email=unicode(self.ws[cabeceras['alumno_3'] + str(i)].value)) if (
            cabeceras.get('alumno_3') and self.ws[cabeceras['alumno_3'] + str(i)].value) else None
        self.tfg['alumno_3'] = data_tfg.get('alumno_3').email if data_tfg.get('alumno_3') else None


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
