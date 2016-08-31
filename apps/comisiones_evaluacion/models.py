from django.db import models
from authentication.models import Profesor
from tfgs.models import Tfg_Asig, Titulacion
from eventos.models import Convocatoria
from django.contrib.auth.models import BaseUserManager
from datetime import datetime


class Comision_EvaluacionManager(BaseUserManager):

    def create(self, **kwargs):
        try:

            try:
                presidente = Profesor.objects.get(email=kwargs.get('presidente'))
            except Profesor.DoesNotExist:
                return dict(status=False, message='El presidente no existe')

            try:
                vocal_1 = Profesor.objects.get(email=kwargs.get('vocal_1'))
            except Profesor.DoesNotExist:
                return dict(status=False, message='El primer titular no existe')

            try:
                vocal_2 = Profesor.objects.get(email=kwargs.get('vocal_2'))
            except Profesor.DoesNotExist:
                return dict(status=False, message='El segundo titular no existe')

            try:
                suplente_1 = Profesor.objects.get(email=kwargs.get('suplente_1'))
            except Profesor.DoesNotExist:
                return dict(status=False, message='El primer suplente no existe')

            try:
                suplente_2 = Profesor.objects.get(email=kwargs.get('suplente_2'))
            except Profesor.DoesNotExist:
                return dict(status=False, message='El segundo suplente no existe')

            try:
                convocatoria = Convocatoria.objects.get(tipo=kwargs.get('convocatoria'), anio=kwargs.get('anio'))
            except Convocatoria.DoesNotExist:
                return dict(status=False, message='La Convocatoria no existe')

            try:
                titulacion = Titulacion.objects.get(codigo=kwargs.get('titulacion'))
            except Convocatoria.DoesNotExist:
                return dict(status=False, message='La titulacion no existe')

            comision = self.model(presidente=presidente, vocal_1=vocal_1, vocal_2=vocal_2, suplente_1=suplente_1,
                                  suplente_2=suplente_2, convocatoria=convocatoria, titulacion=titulacion)

            comision.save()
            return dict(status=True, data=Comision_Evaluacion.objects.get(presidente=comision.presidente))

        except NameError as e:
            return dict(status=False, message=e.message)


class Comision_Evaluacion(models.Model):
    presidente = models.ForeignKey(Profesor, related_name='presidente', default=None)
    vocal_1 = models.ForeignKey(Profesor, related_name='vocal_1', default=None)
    vocal_2 = models.ForeignKey(Profesor, related_name='vocal_2', default=None, null=True)
    suplente_1 = models.ForeignKey(Profesor, related_name='suplente_1', default=None)
    suplente_2 = models.ForeignKey(Profesor, related_name='suplente_2', default=None, null=True)
    convocatoria = models.ForeignKey(Convocatoria, related_name='conv_comision', default=None)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = Comision_EvaluacionManager()

    USERNAME_FIELD = 'presidente'
    REQUIRED_FIELD = USERNAME_FIELD

    def __unicode__(self):
        return self.presidente

    def get_vocal_1(self):
        return self.vocal_1

    def get_vocal_2(self):
        return self.vocal_2

    def get_suplente_1(self):
        return self.suplente_1

    def to_dict(self, user):
        return dict(presidente=self.presidente.to_dict(user), vocal_1=self.vocal_1.to_dict(user),
                    vocal_2=self.vocal_2.to_dict(user), suplente_1=self.suplente_1.to_dict(user),
                    suplente_2=self.suplente_2.to_dict(user), created_at=self.created_at,
                    updated_at=self.updated_at)


class TribunalesManager(BaseUserManager):

    def create(self, **kwargs):
        try:

            try:
                tfg = Tfg_Asig.objects.get(tfg=kwargs.get('tfg'))
            except Tfg_Asig.DoesNotExist:
                return dict(status=False, message='El tfg no existe')

            try:
                comision = Comision_Evaluacion.objects.get(presidente=
                                                           Profesor.objects.get(email=kwargs.get('comision')))
            except Comision_Evaluacion.DoesNotExist:
                return dict(status=False, message='La comision no existe')

            try:
                fecha = datetime.strptime(kwargs.get('fecha'), '%Y-%m-%dT%H:%M:%S') if kwargs.get('fecha') else None
            except:
                raise NameError("Error en la fecha")

            try:
                observaciones = kwargs.get('observaciones')
            except:
                raise NameError("Error en las kwargs.get('fecha')")
            tribunal = self.model(tfg=tfg, comision=comision, fecha=fecha, observaciones=observaciones)
            tribunal.save()
            return dict(status=True, data=Tribunales.objects.get(tfg=tribunal.tfg))

        except NameError as e:
            return dict(status=False, message=e.message)


class Tribunales(models.Model):
    tfg = models.ForeignKey(Tfg_Asig, default=None)
    comision = models.ForeignKey(Comision_Evaluacion, default=None)
    fecha = models.DateTimeField(null=True)
    observaciones = models.CharField(max_length=500, null=True)
    documentacion = models.CharField(max_length=200, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TribunalesManager()

    USERNAME_FIELD = 'tfg'
    REQUIRED_FIELD = USERNAME_FIELD

    def __unicode__(self):
        return self.tfg

    def get_comision(self):
        return self.comision

    def get_fecha(self):
        return self.fecha

    def get_hora(self):
        return self.hora

    def get_observaciones(self):
        return self.observaciones

    def to_dict(self, user):
        return dict(tfg=self.tfg.to_dict(user), comision=self.comision.to_dict(user),
                    fecha=self.fecha, observaciones=self.observaciones,
                    documentacion=self.documentacion, created_at=self.created_at,
                    updated_at=self.updated_at)
