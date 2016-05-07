from django.db.models.signals import post_migrate, post_syncdb
from django.dispatch import receiver
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType


@receiver(post_migrate)
def create_groups(sender, **kwargs):
    from authentication.models import Grupos
    group, created = Grupos.objects.get_or_create(name='Profesores', code=20)
    load_permission_profesores(group)
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


def load_permission_profesores(group):
    content, created = ContentType.objects.get_or_create(app_label='tfgs', model='tfg')
    can_create_tfgs, created = Permission.objects.get_or_create(content_type=content, codename='tfg.create',
                                                                name='Puede crear tfgs')
    group.permissions.add(can_create_tfgs)

    content, created = ContentType.objects.get_or_create(app_label='eventos', model='evento')
    can_create_events, created = Permission.objects.get_or_create(content_type=content, codename='evento.create',
                                                                name='Puede crear eventos')
    group.permissions.add(can_create_tfgs)