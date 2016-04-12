from django.db.models.signals import post_migrate, post_syncdb
from django.dispatch import receiver
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType


@receiver(post_migrate)
def create_groups(sender, **kwargs):
    group, created = Group.objects.get_or_create(name='Profesores')
    load_permission_profesores(group)
    if created:
        print "Group %s created successfully\n" % group.name
    else:
        print "Group %s already exists\n" % group.name

    group, created = Group.objects.get_or_create(name='Alumnos')
    if created:
        print "Group %s created successfully\n" % group.name
    else:
        print "Group %s already exists\n" % group.name


post_migrate.connect(create_groups)


def load_permission_profesores(group):
    content, created = ContentType.objects.get_or_create(app_label='authentication', model='alumno')
    can_get_all, created = Permission.objects.get_or_create(content_type=content, codename='alumns_can_get_all', name='Puede consultar todos los alumnos')
    group.permissions.add(can_get_all)