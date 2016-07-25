from django.contrib.auth.models import BaseUserManager
from django.db import models
from authentication.models import Usuario
from eventtools.models import BaseEvent, BaseOccurrence
from datetime import datetime

try:
    from gestfg.settings import CONVOCATORIAS
except:
    CONVOCATORIAS = ['CONV_JUN', 'CONV_SEPT', 'CONV_DIC']


class Tipo_EventoManager(BaseUserManager):
    def create_tipo_evento(self, **kwargs):
        return self.model.objects.create(**kwargs)


class Tipo_Evento(models.Model):
    nombre = models.CharField(default=None, null=True, max_length=100)
    codigo = models.CharField(default=None, unique=True, null=True, max_length=20)
    objects = Tipo_EventoManager()

    USERNAME_FIELD = 'codigo'
    REQUIRED_FIELD = USERNAME_FIELD

    def __unicode__(self):
        return self.codigo


class EventoManager(models.Manager):

    def create_evento(self, contenido, **kwargs):
        try:
            # Compruebo si tiene autor
            if not isinstance(kwargs.get('autor'), Usuario):
                raise NameError("Autor no valido")

            if not kwargs.get('tipo'):
                raise NameError("Tipo necesario")
            else:
                res = Tipo_Evento.objects.filter(codigo=kwargs.get('tipo'))
                if res.count() == 0:
                    raise NameError("El Tipo no existe")

            evento = Evento.objects.create(contenido=contenido, autor=kwargs.get('autor'),
                                           tipo=kwargs.get('tipo'), titulo=kwargs.get('titulo'))
            evento.save()
            if kwargs.get('tipo').codigo in CONVOCATORIAS:
                convocatoria = Periodo.objects.create(
                    evento=evento,
                    start=datetime.strptime(kwargs.get('desde'), '%d/%m/%Y') if kwargs.get('desde') else None,
                    end=datetime.strptime(kwargs.get('hasta'), '%d/%m/%Y') if kwargs.get('desde') else None)
                convocatoria.save()

            return dict(status=True, data=evento)

        except NameError as e:
            return dict(status=False, message=e.message)


class Evento(BaseEvent):
    autor = models.ForeignKey(Usuario)
    titulo = models.CharField(max_length=50, blank=True)
    contenido = models.TextField()
    tipo = models.ForeignKey(Tipo_Evento, related_name='tipo_evento', default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = EventoManager()

    USERNAME_FIELD = 'contenido'
    REQUIRED_FIELD = USERNAME_FIELD

    def __unicode__(self):
        return '{0}'.format(self.content)

    def get_autor(self):
        return self.autor

    def get_tipo(self):
        return self.tipo

    def get_titulo(self):
        return self.titulo


class Periodo(BaseOccurrence):
    evento = models.ForeignKey(Evento)
