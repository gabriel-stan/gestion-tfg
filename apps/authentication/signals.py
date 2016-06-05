from django.db.models.signals import post_migrate, post_syncdb
from django.dispatch import receiver
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

PERMISOS_PROFESORES={'tfgs': {'tfg': ['create', 'select', 'change', 'delete']},
                     'eventos': {'evento': ['create', 'select', 'change', 'delete']}}


@receiver(post_migrate)
def create_groups(sender, **kwargs):
    from authentication.models import Grupos
    group, created = Grupos.objects.get_or_create(name='Admins', code=10)
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
    if created:
        print "Group %s created successfully\n" % group.name
    else:
        print "Group %s already exists\n" % group.name


post_migrate.connect(create_groups)


def load_permission(group, permissions):
    for app, dict_permission in permissions.items():
        for model, perms in dict_permission.items():
            for i in perms:
                content, created = ContentType.objects.get_or_create(app_label=app, model=model)
                codename = "%s.%s" % (model, i)
                new_perm, created = Permission.objects.get_or_create(content_type=content, codename=codename,
                                                                     name=codename)
                group.permissions.add(new_perm)
