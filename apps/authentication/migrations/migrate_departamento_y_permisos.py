# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_auto_20160605_1421'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profesor',
            name='departamento'
        ),

        migrations.AddField(
            model_name='profesor',
            name='departamento',
            field=models.ForeignKey(related_name='departamento', default=None, to=settings.AUTH_USER_MODEL, null=True),
        ),

        migrations.RunSQL("DELETE FROM auth_group_permissions"),
        migrations.RunSQL("DELETE FROM auth_permission WHERE codename='tfg.create' OR codename='evento.create'")
    ]
