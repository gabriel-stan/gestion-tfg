from django.contrib.auth.models import BaseUserManager
from django.db import models
from authentication.models import Usuario
from eventtools.models import BaseEvent, BaseOccurrence
import datetime

YEAR_CHOICES = []
for r in range(1980, (datetime.datetime.now().year+1)):
    YEAR_CHOICES.append((r,r))

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

    def to_dict(self):
        return dict(nombre=self.nombre, codigo=self.codigo)


class ConvocatoriaManager(BaseUserManager):
    def create_convocatoria(self, **kwargs):
        return self.model.objects.create(**kwargs)


class Convocatoria(models.Model):
    anio = models.IntegerField('anio', choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    tipo = models.ForeignKey(Tipo_Evento, related_name='convocatoria_tipo', default=None, null=True)
    objects = ConvocatoriaManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELD = USERNAME_FIELD

    def __unicode__(self):
        return self.id

    def to_dict(self):
        return dict(anio=self.anio, tipo=self.tipo.to_dict())


class SubTipo_EventoManager(BaseUserManager):
    def create_tipo_evento(self, **kwargs):
        return self.model.objects.create(**kwargs)


class SubTipo_Evento(models.Model):
    nombre = models.CharField(default=None, null=True, max_length=100)
    codigo = models.CharField(default=None, null=True, max_length=20)
    objects = Tipo_EventoManager()

    USERNAME_FIELD = 'codigo'
    REQUIRED_FIELD = USERNAME_FIELD

    def __unicode__(self):
        return self.codigo

    def to_dict(self):
        return dict(nombre=self.nombre, codigo=self.codigo)


class EventoManager(models.Manager):

    def create_evento(self, contenido, **kwargs):
        try:
            convocatoria = None
            # Compruebo si tiene autor
            if not isinstance(kwargs.get('autor'), Usuario):
                raise NameError("Autor no valido")

            if not kwargs.get('convocatoria'):
                raise NameError("Convocatoria necesaria")
            elif kwargs.get('convocatoria') in CONVOCATORIAS:
                anio = datetime.datetime.strptime(kwargs.get('desde')[:19], '%Y-%m-%dT%H:%M:%S').year
                convocatoria = Convocatoria.objects.filter(tipo=Tipo_Evento.objects.get(codigo=kwargs.get('convocatoria')), anio=anio)
                if convocatoria.count() == 0:
                    raise NameError("La Convocatoria no existe")

            if kwargs.get('convocatoria') not in CONVOCATORIAS:
                tipo = None
            elif not kwargs.get('tipo'):
                    raise NameError("Tipo necesario")
            else:
                res = SubTipo_Evento.objects.filter(codigo=kwargs.get('tipo'))
                if res.count() != 1:
                    raise NameError("El SubTipo no existe")
                tipo=res[0]

            evento = Evento.objects.create(contenido=contenido, autor=kwargs.get('autor'),
                                           tipo=tipo, convocatoria=convocatoria[0] if convocatoria else None, titulo=kwargs.get('titulo'))
            evento.save()
            if kwargs.get('convocatoria') in CONVOCATORIAS:
                convocatoria = Periodo.objects.create(
                    evento=evento,
                    start=datetime.datetime.strptime(kwargs.get('desde')[:19], '%Y-%m-%dT%H:%M:%S') if kwargs.get('desde') else
                    None,
                    end=datetime.datetime.strptime(kwargs.get('hasta')[:19], '%Y-%m-%dT%H:%M:%S') if kwargs.get('hasta') else
                    None)
                convocatoria.save()

            return dict(status=True, data=evento)

        except NameError as e:
            return dict(status=False, message=e.message)


class Evento(BaseEvent):
    autor = models.ForeignKey(Usuario)
    titulo = models.CharField(max_length=50, blank=True)
    contenido = models.TextField()
    tipo = models.ForeignKey(SubTipo_Evento, related_name='tipo', default=None, null=True)
    convocatoria = models.ForeignKey(Convocatoria, related_name='conv_evento', default=None, null=True)
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
