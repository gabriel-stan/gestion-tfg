from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType


@receiver(post_migrate)
def create_groups(sender, **kwargs):
    group, created = Group.objects.get_or_create(name='Profesores')
    #load_permission_profesores(group)
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


# def load_permission_profesores(group):
#     content_type = ContentType.objects.get(model='profesor')
#     permission = Permission.objects.create(codename='can_get_alumnos',
#                                            name='Puede obtener los datos de alumno/s',
#                                            content_type=content_type)
#     group.permissions.add(permission)
