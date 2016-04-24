from django.db import models
from authentication.models import Usuario


class EventoManager(models.Manager):

    def create_evento(self, contenido, **kwargs):
        try:
            # Compruebo si tiene autor
            if not isinstance(kwargs.get('autor'), Usuario):
                raise NameError("Autor no valido")

            evento = Evento.objects.create(contenido=contenido, autor=kwargs.get('autor'),
                                           tipo=kwargs.get('tipo'))
            evento.save()

            return dict(status=True, data=Evento.objects.get(contenido=contenido))

        except NameError as e:
            return dict(status=False, message=e.message)


class Evento(models.Model):
    autor = models.ForeignKey(Usuario)
    contenido = models.TextField()
    tipo = models.CharField(max_length=100)
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
