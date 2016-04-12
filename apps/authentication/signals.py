from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User, Group, Permission
from guardian.shortcuts import assign_perm


@receiver(post_migrate)
def create_groups(sender, **kwargs):
    group, created = Group.objects.get_or_create(name='Profesores')
    if created:
        print "Group %s created successfully\n" % group.name
    else:
        print "Group %s already exists\n" % group.name

    group, created = Group.objects.get_or_create(name='Alumnos')
    load_permission_alumnos(group)
    if created:
        print "Group %s created successfully\n" % group.name
    else:
        print "Group %s already exists\n" % group.name


post_migrate.connect(create_groups)


def load_permission_alumnos(group):
    from authentication.models import Alumno
    assign_perm("authenticate.can_login", group)