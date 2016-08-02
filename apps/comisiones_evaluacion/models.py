from django.db import models
from authentication.models import Profesor
from django.contrib.auth.models import BaseUserManager


class Comision_EvaluacionManager(BaseUserManager):

    def create(self, **kwargs):
        try:

            try:
                presidente = Profesor.objects.get(email=kwargs.get('presidente'))
            except Profesor.DoesNotExist:
                return dict(status=False, message='El presidente no existe')

            if kwargs.get('suplente') and kwargs.get('suplente') is not '':
                try:
                    suplente = Profesor.objects.get(email=kwargs.get('suplente'))
                except Profesor.DoesNotExist:
                    return dict(status=False, message='El sustituto del presidente no existe')

            try:
                vocal_1 = Profesor.objects.get(email=kwargs.get('vocal_1'))
            except Profesor.DoesNotExist:
                return dict(status=False, message='El primer titular no existe')

            try:
                vocal_2 = Profesor.objects.get(email=kwargs.get('vocal_2'))
            except Profesor.DoesNotExist:
                return dict(status=False, message='El segundo titular no existe')

            if kwargs.get('suplente') and kwargs.get('suplente') is not '':
                try:
                    suplente = Profesor.objects.get(email=kwargs.get('suplente'))
                    comision = self.model(presidente=presidente, vocal_1=vocal_1, vocal_2=vocal_2,
                                  suplente=suplente)
                except Profesor.DoesNotExist:
                    return dict(status=False, message='El sustituto del presidente no existe')
            else:
                comision = self.model(presidente=presidente, vocal_1=vocal_1, vocal_2=vocal_2)

            comision.save()
            return dict(status=True, data=Comision_Evaluacion.objects.get(presidente=comision.presidente))

        except NameError as e:
            return dict(status=False, message=e.message)


class Comision_Evaluacion(models.Model):
    presidente = models.ForeignKey(Profesor, related_name='presidente', default=None)
    vocal_1 = models.ForeignKey(Profesor, related_name='vocal_1', default=None)
    vocal_2 = models.ForeignKey(Profesor, related_name='vocal_2', default=None, null=True)
    suplente = models.ForeignKey(Profesor, related_name='suplente', default=None)

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

    def get_suplente(self):
        return self.suplente

