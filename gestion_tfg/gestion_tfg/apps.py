from django.apps import AppConfig

class GestionTFGConfig(AppConfig):
    name = 'gestion_tfg'

    def ready(self):
        import gestion_tfg.signals