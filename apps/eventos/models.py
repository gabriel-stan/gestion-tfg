from django.db import models
from authentication.models import Usuario


class EventoManager(models.Manager):

    def create_evento(self, contenido, **kwargs):
        try:
            # Compruebo si tiene autor
            if not isinstance(kwargs.get('autor'), Usuario):
                raise NameError("Autor no valido")

            evento = Evento.objects.create(contenido=contenido, autor=kwargs.get('autor'),
                                           tipo=kwargs.get('tipo'), titulo=kwargs.get('titulo'))
            evento.save()

            return dict(status=True, data=evento)

        except NameError as e:
            return dict(status=False, message=e.message)


class Evento(models.Model):
    autor = models.ForeignKey(Usuario)
    titulo = models.CharField(max_length=50, blank=True)
    #autor = models.ForeignKey(Usuario, related_name='eventos')
    contenido = models.TextField()
    tipo = models.CharField(max_length=100, blank=True)
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
