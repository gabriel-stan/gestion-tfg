from django.db.models.signals import post_migrate, post_syncdb
from django.dispatch import receiver
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType


PERMISOS_JEFE_DEPARTAMENTO={'tfgs': {'tfg': ['create', 'select', 'change', 'delete', 'masivos']},
                             'eventos': {'evento': ['create', 'select', 'change', 'delete']},
                             'authentication': {'usuario': ['select']}}

PERMISOS_PROFESORES={'tfgs': {'tfg': ['create', 'select', 'change', 'delete']},
                     'eventos': {'evento': ['create', 'select', 'change', 'delete']},
                     'authentication': {'usuario': ['select']}}

PERMISOS_ALUMNOS={'tfgs': {'tfg': ['select']}}

PERMISOS_USUARIOS={'tfgs': {'tfg': ['select']}}



@receiver(post_migrate)
def create_groups(sender, **kwargs):
    from authentication.models import Grupos
    group, created = Grupos.objects.get_or_create(name='Administrador', code=10)
    if created:
        print "Group %s created successfully\n" % group.name
    else:
        print "Group %s already exists\n" % group.name

    group, created = Grupos.objects.get_or_create(name='Profesores', code=20)
    load_permission(group, PERMISOS_PROFESORES)
    if created:
        print "Group %s created successfully\n" % group.name
    else:
        print "Group %s already exists\n" % group.name

    group, created = Grupos.objects.get_or_create(name='Alumnos', code=30)
    load_permission(group, PERMISOS_ALUMNOS)
    if created:
        print "Group %s created successfully\n" % group.name
    else:
        print "Group %s already exists\n" % group.name

    group, created = Grupos.objects.get_or_create(name='Jefe de Departamento', code=40)
    load_permission(group, PERMISOS_JEFE_DEPARTAMENTO)
    if created:
        print "Group %s created successfully\n" % group.name
    else:
        print "Group %s already exists\n" % group.name

    from eventos.models import Tipo_Evento
    tipo, created = Tipo_Evento.objects.get_or_create(nombre='Convocatoria de Junio', codigo='CONV_JUN')
    if created:
        print "Tipo de evento %s created successfully\n" % tipo.nombre
    else:
        print "Tipo de evento %s already exists\n" % tipo.nombre

    tipo, created = Tipo_Evento.objects.get_or_create(nombre='Convocatoria de Septiembre', codigo='CONV_SEPT')
    if created:
        print "Tipo de evento %s created successfully\n" % tipo.nombre
    else:
        print "Tipo de evento %s already exists\n" % tipo.nombre

    tipo, created = Tipo_Evento.objects.get_or_create(nombre='Convocatoria de Diciembre', codigo='CONV_DIC')
    if created:
        print "Tipo de evento %s created successfully\n" % tipo.nombre
    else:
        print "Tipo de evento %s already exists\n" % tipo.nombre
post_migrate.connect(create_groups)


def load_permission(group, permissions):
    for app, dict_permission in permissions.items():
        for model, perms in dict_permission.items():
            for i in perms:
                content, created = ContentType.objects.get_or_create(app_label=app, model=model)
                codename = "%s.%s" % (model, i)
                new_perm, created = Permission.objects.get_or_create(content_type=content, codename=codename,
                                                                     name=codename)
                if not created:
                    group.permissions.add(new_perm)
