__author__ = 'tonima'
from openpyxl import load_workbook
from authentication.models import Profesor, Alumno
from tfgs.models import Titulacion, Tfg_Asig, Tfg


class Tfgs_masivos(object):

    def __init__(self, fichero=None):
        if fichero:
            self.wb = load_workbook(fichero)
            self.ws = self.wb.active
        self.errores = []
        self.exitos = []

    def upload_file_tfg(self, u_fila, p_fila, cabeceras, titulacion):
        for i in range(p_fila, u_fila+1):
            try:
                data_tfg = self.read_data(cabeceras, i)
                self.tfg = self.check_tfg(data_tfg, i,titulacion)
                if self.tfg is not False and Tfg.objects.simular_create_tfg(**self.tfg):
                    self.exitos.append(dict(fila=i, tfg=self.tfg))
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

    def check_tfg(self, tfg, i, titulacion):
        if not tfg.get('titulo'):
            self.errores.append(dict(fila=i, message='El TFG no tiene titulo'))
            return False
        tfg['tutor'] = Profesor.objects.get(email=tfg.get('tutor'))
        tfg['titulacion'] = Titulacion.objects.get(codigo=titulacion)
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

    def upload_file_confirm(self, tfgs):
        errores = []
        for index, data_tfg in enumerate(tfgs):
            try:
                tfg = data_tfg.get('tfg')
                res = Tfg.objects.create(**tfg)
                if not res.get('status'):
                    errores.append(dict(fila=index, tfg=tfg))
            except Exception as e:
                errores.append(dict(fila=index, message=e.message))
                continue
        return dict(status=True, errores=errores)


class Tfgs_asig_masivos(Tfgs_masivos):

    def __init__(self, fichero=None):
        super(Tfgs_asig_masivos, self).__init__(fichero)

    def upload_file_tfg(self, u_fila, p_fila, cabeceras, titulacion):
        for i in range(p_fila, u_fila+1):
            try:
                data_tfg = self.read_data(cabeceras, i)
                self.tfg = self.check_tfg(data_tfg, i, titulacion)
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
        data_tfg['alumno_1'] = Alumno(email=unicode(self.ws[cabeceras['alumno_1'] + str(i)].value if
                                                    cabeceras.get('alumno_1') else None))
        self.tfg['alumno_1'] = data_tfg.get('alumno_1').email if data_tfg.get('alumno_1') else None

        data_tfg['alumno_2'] = Alumno(email=unicode(self.ws[cabeceras['alumno_2'] + str(i)].value)) if (
            cabeceras.get('alumno_2') and self.ws[cabeceras['alumno_2'] + str(i)].value) else None
        self.tfg['alumno_2'] = data_tfg.get('alumno_2').email if data_tfg.get('alumno_2') else None

        data_tfg['alumno_3'] = Alumno(email=unicode(self.ws[cabeceras['alumno_3'] + str(i)].value)) if (
            cabeceras.get('alumno_3') and self.ws[cabeceras['alumno_3'] + str(i)].value) else None
        self.tfg['alumno_3'] = data_tfg.get('alumno_3').email if data_tfg.get('alumno_3') else None

    def upload_file_confirm(self, tfgs):
        errores = []
        for index, data_tfg in enumerate(tfgs):
            try:
                self.alumno_1 = self.get_or_create_alumno(email=data_tfg['tfg'].get('alumno_1')) if data_tfg['tfg']\
                    .get('alumno_1') else None
                self.alumno_2 = self.get_or_create_alumno(email=data_tfg['tfg'].get('alumno_2')) if data_tfg['tfg']\
                    .get('alumno_2') else None
                self.alumno_3 = self.get_or_create_alumno(email=data_tfg['tfg'].get('alumno_3')) if data_tfg['tfg']\
                    .get('alumno_3') else None
                self.tfg = Tfg.objects.create(**data_tfg['tfg'])
                res = Tfg_Asig.objects.create(tfg=self.tfg.get('data'), alumno_1=self.alumno_1, alumno_2=self.alumno_2,
                                           alumno_3=self.alumno_3)
                if not res.get('status'):
                    errores.append(dict(fila=index, tfg=data_tfg))
            except Exception as e:
                errores.append(dict(fila=index, message=e.message))
                continue
        return dict(status=True, errores=errores)

    def get_or_create_alumno(self, email):
        if not Alumno.objects.filter(email=email if email else None).exists():
            Alumno.objects.create_user(email=email)
        try:
            return Alumno.objects.get(email=email)
        except Alumno.DoesNotExist:
            raise NameError("Error en el alumno %s" % email)