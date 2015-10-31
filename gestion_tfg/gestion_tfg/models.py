from django.db import models


class tfg(models.Model):
    tipo = models.CharField(max_length=100)
    titulo = models.CharField(max_length=100)
    n_ala = models.IntegerField()
    descripcion = models.TextField()
    conocimientos_previos = models.CharField(max_length=100)
    hard_soft = models.CharField(max_length=100)
    # tutor = models.ForeignKey('usuario', related_name='tutor')
    # cotutor = models.ForeignKey('usuario', related_name='cotutor')