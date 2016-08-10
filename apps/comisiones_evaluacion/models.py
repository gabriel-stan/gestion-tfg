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

            try:
                vocal_1 = Profesor.objects.get(email=kwargs.get('vocal_1'))
            except Profesor.DoesNotExist:
                return dict(status=False, message='El primer titular no existe')

            try:
                vocal_2 = Profesor.objects.get(email=kwargs.get('vocal_2'))
            except Profesor.DoesNotExist:
                return dict(status=False, message='El segundo titular no existe')

            if kwargs.get('suplente_1') and kwargs.get('suplente_1') is not '':
                try:
                    suplente_1 = Profesor.objects.get(email=kwargs.get('suplente_1'))
                    comision = self.model(presidente=presidente, vocal_1=vocal_1, vocal_2=vocal_2,
                                          suplente_1=suplente_1)
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
    suplente_1 = models.ForeignKey(Profesor, related_name='suplente_1', default=None)
    suplente_2 = models.ForeignKey(Profesor, related_name='suplente_2', default=None, null=True)

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

