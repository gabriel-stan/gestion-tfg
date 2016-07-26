from django.db import models
from authentication.models import Profesor
from django.contrib.auth.models import BaseUserManager
from services import Comision


class Comision_EvaluacionManager(BaseUserManager):

    def create(self, **kwargs):
        try:

            try:
                presidente = Profesor.objects.get(email=kwargs.get('presidente'))
            except Profesor.DoesNotExist:
                return dict(status=False, message='El presidente no existe')

            try:
                sup_presidente = Profesor.objects.get(email=kwargs.get('sup_presidente'))
            except Profesor.DoesNotExist:
                return dict(status=False, message='El sustituto del presidente no existe')

            try:
                titular_1 = Profesor.objects.get(email=kwargs.get('titular_1'))
            except Profesor.DoesNotExist:
                return dict(status=False, message='El primer titular no existe')

            try:
                titular_2 = Profesor.objects.get(email=kwargs.get('titular_2'))
            except Profesor.DoesNotExist:
                return dict(status=False, message='El segundo titular no existe')

            if kwargs.get('sup_titular_1'):
                try:
                    sup_titular_1 = Profesor.objects.get(email=kwargs.get('sup_titular_1'))
                except Profesor.DoesNotExist:
                    return dict(status=False, message='El sustituto del primer titular no existe')
            else:
                sup_titular_1 = None

            if kwargs.get('sup_titular_2'):
                try:
                    sup_titular_2 = Profesor.objects.get(email=kwargs.get('sup_titular_2'))
                except Profesor.DoesNotExist:
                    return dict(status=False, message='El sustituto del segundo titular no existe')
            else:
                sup_titular_2 = None

            comision = self.model(presidente=presidente, titular_1=titular_1, titular_2=titular_2,
                                  sup_presidente=sup_presidente, sup_titular_1=sup_titular_1,
                                  sup_titular_2=sup_titular_2)

            comision.save()
            return dict(status=True, data=Comision_Evaluacion.objects.get(presidente=comision.presidente))

        except NameError as e:
            return dict(status=False, message=e.message)

    def create_file(self, **kwargs):
        try:
            presidente = Profesor.objects.get(email=kwargs.get('presidente'))
            sup_presidente = Profesor.objects.get(email=kwargs.get('sup_presidente'))
            titular_1 = Profesor.objects.get(email=kwargs.get('titular_1'))
            sup_titular_1 = Profesor.objects.get(email=kwargs.get('sup_titular_1'))
            if kwargs.get('titular_2'):
                titular_2 = Profesor.objects.get(email=kwargs.get('titular_2'))
                sup_titular_2 = Profesor.objects.get(email=kwargs.get('sup_titular_2'))
            else:
                titular_2 = None
                sup_titular_2 = None

            comision = self.model(presidente=presidente, titular_1=titular_1, titular_2=titular_2,
                                  sup_presidente=sup_presidente, sup_titular_1=sup_titular_1,
                                  sup_titular_2=sup_titular_2)

            comision.save()
            return dict(status=True, data=Comision_Evaluacion.objects.get(id=comision.id))

        except NameError as e:
            return dict(status=False, message=e.message)


class Comision_Evaluacion(models.Model):
    presidente = models.ForeignKey(Profesor, related_name='presidente', default=None)
    titular_1 = models.ForeignKey(Profesor, related_name='titular_1', default=None)
    titular_2 = models.ForeignKey(Profesor, related_name='titular_2', default=None, null=True)
    sup_presidente = models.ForeignKey(Profesor, related_name='sup_presidente', default=None)
    sup_titular_1 = models.ForeignKey(Profesor, related_name='sup_titular_1', default=None, null=True)
    sup_titular_2 = models.ForeignKey(Profesor, related_name='sup_titular_2', default=None, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = Comision_EvaluacionManager()

    USERNAME_FIELD = 'presidente'
    REQUIRED_FIELD = USERNAME_FIELD

    def __unicode__(self):
        return self.presidente

    def get_titular_1(self):
        return self.titular_1

    def get_titular_2(self):
        return self.titular_2

    def get_sup_presidente(self):
        return self.sup_presidente

    def get_sup_titular_1(self):
        return self.sup_titular_1

    def get_sup_titular_2(self):
        return self.sup_titular_2
